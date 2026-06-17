import sqlite3

from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.sqlite_append_engine import (
    SQLiteAppendEngine,
)

from phase2.sqlite_ledger.sqlite_integrity_verifier import (
    SQLiteIntegrityVerifier,
)


def test_accepts_valid_sqlite_ledger(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    appender = SQLiteAppendEngine(
        db_path
    )

    appender.append(
        lsn=1,
        opcode="EVENT_A",
        payload={
            "id": "event-001",
        },
    )

    appender.append(
        lsn=2,
        opcode="EVENT_B",
        payload={
            "id": "event-002",
        },
    )

    verifier = SQLiteIntegrityVerifier(
        db_path
    )

    assert verifier.verify()


def test_detects_payload_tampering(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    appender = SQLiteAppendEngine(
        db_path
    )

    appender.append(
        lsn=1,
        opcode="EVENT_A",
        payload={
            "id": "event-001",
        },
    )

    connection = sqlite3.connect(
        db_path
    )

    connection.execute(
        """
        UPDATE wal_records
        SET payload_json = ?
        WHERE lsn = ?
        """,
        (
            '{"id":"forged"}',
            1,
        ),
    )

    connection.commit()
    connection.close()

    verifier = SQLiteIntegrityVerifier(
        db_path
    )

    assert not verifier.verify()


def test_detects_previous_hash_tampering(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    appender = SQLiteAppendEngine(
        db_path
    )

    appender.append(
        lsn=1,
        opcode="EVENT_A",
        payload={},
    )

    appender.append(
        lsn=2,
        opcode="EVENT_B",
        payload={},
    )

    connection = sqlite3.connect(
        db_path
    )

    connection.execute(
        """
        UPDATE wal_records
        SET previous_hash = ?
        WHERE lsn = ?
        """,
        (
            "BROKEN_HASH",
            2,
        ),
    )

    connection.commit()
    connection.close()

    verifier = SQLiteIntegrityVerifier(
        db_path
    )

    assert not verifier.verify()
