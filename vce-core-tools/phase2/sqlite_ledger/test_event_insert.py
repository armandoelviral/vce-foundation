import sqlite3

from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.event_insert import (
    EventInsert,
)


def test_insert_creates_one_row(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    inserter = EventInsert(
        db_path
    )

    inserter.insert(
        lsn=1,
        opcode="APPEND_EVENT",
        payload_json='{"id":"event-001"}',
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.execute(
        "SELECT COUNT(*) FROM wal_records"
    )

    count = cursor.fetchone()[0]

    connection.close()

    assert count == 1


def test_insert_persists_lsn(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    inserter = EventInsert(
        db_path
    )

    inserter.insert(
        lsn=42,
        opcode="APPEND_EVENT",
        payload_json="{}",
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.execute(
        "SELECT lsn FROM wal_records"
    )

    value = cursor.fetchone()[0]

    connection.close()

    assert value == 42


def test_insert_persists_opcode(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    inserter = EventInsert(
        db_path
    )

    inserter.insert(
        lsn=1,
        opcode="REGISTER_ARTIFACT",
        payload_json="{}",
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.execute(
        "SELECT opcode FROM wal_records"
    )

    opcode = cursor.fetchone()[0]

    connection.close()

    assert opcode == "REGISTER_ARTIFACT"
