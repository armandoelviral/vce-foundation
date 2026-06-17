import sqlite3

from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)


def test_schema_creates_database_file(tmp_path):

    db_path = tmp_path / "ledger.db"

    schema = SQLiteLedgerSchema(
        db_path=db_path,
    )

    schema.initialize()

    assert db_path.exists()


def test_schema_creates_wal_records_table(tmp_path):

    db_path = tmp_path / "ledger.db"

    schema = SQLiteLedgerSchema(
        db_path=db_path,
    )

    schema.initialize()

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='wal_records'"
    )

    result = cursor.fetchone()

    connection.close()

    assert result[0] == "wal_records"


def test_schema_table_has_required_columns(tmp_path):

    db_path = tmp_path / "ledger.db"

    schema = SQLiteLedgerSchema(
        db_path=db_path,
    )

    schema.initialize()

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.execute(
        "PRAGMA table_info(wal_records)"
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    connection.close()

    assert "lsn" in columns
    assert "opcode" in columns
    assert "payload_json" in columns
    assert "previous_hash" in columns
    assert "current_hash" in columns
