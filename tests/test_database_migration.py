from datetime import date

import pytest
from sqlalchemy import Column, ForeignKey, MetaData, String, Table

from backend.migrate_localdb import fingerprint, parent_first


def test_verification_is_order_independent_and_detects_changes():
    first = [{"id": "one", "payload": {"a": 1}, "day": date(2026, 11, 2), "data": b"docx"}]
    assert fingerprint(first) == fingerprint(list(reversed(first)))
    assert fingerprint(first) != fingerprint([{**first[0], "data": b"changed"}])


def test_self_referencing_rows_are_sorted_and_cycles_refused():
    metadata = MetaData()
    table = Table("nodes", metadata, Column("id", String(36), primary_key=True), Column("parent_id", String(36), ForeignKey("nodes.id")))
    parent = {"id": "parent", "parent_id": None}
    child = {"id": "child", "parent_id": "parent"}
    assert parent_first([child, parent], table) == [parent, child]
    with pytest.raises(ValueError, match="Cycle or missing parent"):
        parent_first([{"id": "a", "parent_id": "b"}, {"id": "b", "parent_id": "a"}], table)
