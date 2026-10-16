"""One-time, verified copy from the preserved SQLite file to an empty LocalDB."""
import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone

from sqlalchemy import inspect, select

import backend.models
from backend.config import DB_PATH
from backend.database import Base, create_database_engine
from backend.sqlserver import install_delete_triggers, localdb_url


def fingerprint(rows: list[dict]) -> str:
    def serialize(value):
        if isinstance(value, bytes):
            return {"binary_sha256": hashlib.sha256(value).hexdigest()}
        if hasattr(value, "isoformat"):
            return value.isoformat()
        raise TypeError(f"Unsupported migration value: {type(value).__name__}")
    canonical = sorted(json.dumps(row, sort_keys=True, default=serialize, ensure_ascii=True) for row in rows)
    return hashlib.sha256("\n".join(canonical).encode("utf-8")).hexdigest()


def parent_first(rows: list[dict], table) -> list[dict]:
    links = [foreign_key for foreign_key in table.foreign_keys if foreign_key.column.table is table]
    if not links:
        return rows
    pending = list(rows)
    ordered = []
    inserted = set()
    primary_key = list(table.primary_key.columns)[0].name
    while pending:
        ready = [row for row in pending if all(
            row[link.parent.name] is None or row[link.parent.name] in inserted for link in links
        )]
        if not ready:
            raise ValueError(f"Cycle or missing parent detected in {table.name}; source is unchanged")
        ordered.extend(ready)
        inserted.update(row[primary_key] for row in ready)
        ready_ids = {row[primary_key] for row in ready}
        pending = [row for row in pending if row[primary_key] not in ready_ids]
    return ordered


def migrate(database: str) -> dict:
    if not DB_PATH.is_file():
        raise ValueError("Source SQLite database does not exist")
    backup_dir = DB_PATH.parent / "exports"
    backup_dir.mkdir(exist_ok=True)
    backup = backup_dir / f"sqlite_before_localdb_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}.db"
    with sqlite3.connect(DB_PATH) as source, sqlite3.connect(backup) as destination:
        source.backup(destination)
        if destination.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("SQLite backup failed integrity verification; migration aborted")
    source_engine = create_database_engine(f"sqlite:///{backup}")
    target_engine = create_database_engine(localdb_url(database))
    counts = {}
    try:
        with source_engine.connect() as source, target_engine.begin() as target:
            if inspect(target).get_table_names():
                raise ValueError("Destination must have no user tables; refusing to overwrite existing SQL data")
            Base.metadata.create_all(target)
            install_delete_triggers(target, Base.metadata)
            for table in Base.metadata.sorted_tables:
                source_rows = [dict(row) for row in source.execute(select(table)).mappings()]
                rows = parent_first(source_rows, table)
                if rows:
                    target.execute(table.insert(), rows)
                target_rows = [dict(row) for row in target.execute(select(table)).mappings()]
                if len(source_rows) != len(target_rows) or fingerprint(source_rows) != fingerprint(target_rows):
                    raise ValueError(f"Data verification failed in {table.name}; destination transaction rolled back")
                counts[table.name] = len(rows)
        return {"database": database, "verified_rows": counts, "sqlite_backup": str(backup), "activated": False}
    finally:
        source_engine.dispose()
        target_engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True)
    args = parser.parse_args()
    print(json.dumps(migrate(args.database), indent=2))
