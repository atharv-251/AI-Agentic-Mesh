from sqlalchemy.dialects.mssql.base import MSDDLCompiler, MSTypeCompiler
from sqlalchemy.engine import URL
from sqlalchemy import String, Text, Unicode, UnicodeText


def localdb_url(database: str) -> URL:
    if not database or len(database) > 128 or any(not (char.isalnum() or char == "_") for char in database):
        raise ValueError("LocalDB database name must contain only letters, numbers and underscores")
    return URL.create("mssql+pyodbc", query={"odbc_connect": (
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=(LocalDB)\\MSSQLLocalDB;"
        f"DATABASE={database};Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes"
    )})


class PlannerDDLCompiler(MSDDLCompiler):
    def define_constraint_cascades(self, constraint):
        # SQL Server disallows this model's multiple cascade paths.
        return ""


class PlannerTypeCompiler(MSTypeCompiler):
    def visit_VARCHAR(self, type_, **kw):
        return self.visit_NVARCHAR(type_, **kw)

    def visit_TEXT(self, type_, **kw):
        return "NVARCHAR(max)"

    def visit_DATETIME(self, type_, **kw):
        return "DATETIME2(6)"


def configure_sqlserver(engine):
    engine.dialect.colspecs = {
        **engine.dialect.colspecs,
        String: engine.dialect.colspecs[Unicode],
        Text: engine.dialect.colspecs[UnicodeText],
    }
    engine.dialect.ddl_compiler = PlannerDDLCompiler
    engine.dialect.type_compiler_instance = PlannerTypeCompiler(engine.dialect)


def install_delete_triggers(connection, metadata):
    """Preserve the model's CASCADE/SET NULL semantics using set-based triggers."""
    quote = connection.dialect.identifier_preparer.quote
    tables = list(metadata.sorted_tables)
    for parent in tables:
        incoming = [
            (child, foreign_key)
            for child in reversed(tables)
            for foreign_key in child.foreign_keys
            if foreign_key.column.table is parent and foreign_key.ondelete in ("CASCADE", "SET NULL")
        ]
        if not incoming:
            continue
        primary_key = list(parent.primary_key.columns)
        if len(primary_key) != 1 or primary_key[0].type.length != 36:
            raise ValueError(f"Delete trigger requires a single UUID primary key: {parent.name}")
        key = quote(primary_key[0].name)
        parent_name = quote(parent.name)
        lines = [
            f"CREATE OR ALTER TRIGGER {quote('kt_delete_' + parent.name)} ON {parent_name}",
            "INSTEAD OF DELETE AS BEGIN",
            "SET NOCOUNT ON;",
            "DECLARE @ids TABLE (id NVARCHAR(36) PRIMARY KEY);",
            f"INSERT INTO @ids SELECT {key} FROM deleted;",
        ]
        self_links = [fk for child, fk in incoming if child is parent and fk.ondelete == "CASCADE"]
        for foreign_key in self_links:
            column = quote(foreign_key.parent.name)
            lines.extend([
                "WHILE 1 = 1 BEGIN",
                f"INSERT INTO @ids SELECT n.{key} FROM {parent_name} n",
                f"WHERE n.{column} IN (SELECT id FROM @ids) AND n.{key} NOT IN (SELECT id FROM @ids);",
                "IF @@ROWCOUNT = 0 BREAK;",
                "END;",
            ])
        for child, foreign_key in incoming:
            if child is parent:
                continue
            child_name = quote(child.name)
            column = quote(foreign_key.parent.name)
            if foreign_key.ondelete == "CASCADE":
                lines.append(f"DELETE FROM {child_name} WHERE {column} IN (SELECT id FROM @ids);")
            else:
                lines.append(f"UPDATE {child_name} SET {column} = NULL WHERE {column} IN (SELECT id FROM @ids);")
        lines.extend([f"DELETE FROM {parent_name} WHERE {key} IN (SELECT id FROM @ids);", "END;"])
        connection.exec_driver_sql("\n".join(lines))
