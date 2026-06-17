from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.event_insert import (
    EventInsert,
)

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)


def test_query_returns_empty_list_for_empty_ledger(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    query = EventQuery(
        db_path
    )

    assert query.all() == []


def test_query_returns_inserted_event(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    EventInsert(
        db_path
    ).insert(
        lsn=1,
        opcode="APPEND_EVENT",
        payload_json='{"id":"event-001"}',
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    query = EventQuery(
        db_path
    )

    rows = query.all()

    assert len(rows) == 1


def test_query_preserves_lsn_order(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    inserter = EventInsert(
        db_path
    )

    inserter.insert(
        lsn=1,
        opcode="EVENT_A",
        payload_json="{}",
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    inserter.insert(
        lsn=2,
        opcode="EVENT_B",
        payload_json="{}",
        previous_hash="hash-001",
        current_hash="hash-002",
    )

    rows = EventQuery(
        db_path
    ).all()

    assert rows[0]["lsn"] == 1
    assert rows[1]["lsn"] == 2


def test_query_returns_opcode(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    EventInsert(
        db_path
    ).insert(
        lsn=1,
        opcode="REGISTER_ARTIFACT",
        payload_json="{}",
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    rows = EventQuery(
        db_path
    ).all()

    assert (
        rows[0]["opcode"]
        == "REGISTER_ARTIFACT"
    )
