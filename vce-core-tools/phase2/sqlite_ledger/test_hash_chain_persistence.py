from phase2.sqlite_ledger.sqlite_schema import (
    SQLiteLedgerSchema,
)

from phase2.sqlite_ledger.event_insert import (
    EventInsert,
)

from phase2.sqlite_ledger.event_query import (
    EventQuery,
)

from phase2.sqlite_ledger.hash_chain_verifier import (
    HashChainVerifier,
)


def test_first_record_uses_genesis_hash(tmp_path):

    db_path = tmp_path / "ledger.db"

    SQLiteLedgerSchema(
        db_path
    ).initialize()

    EventInsert(
        db_path
    ).insert(
        lsn=1,
        opcode="EVENT_A",
        payload_json="{}",
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    rows = EventQuery(
        db_path
    ).all()

    assert (
        rows[0]["previous_hash"]
        == "GENESIS"
    )


def test_hash_chain_links_records(tmp_path):

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

    assert (
        rows[1]["previous_hash"]
        == rows[0]["current_hash"]
    )


def test_verifier_accepts_valid_chain(tmp_path):

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

    verifier = HashChainVerifier(
        db_path
    )

    assert verifier.verify()


def test_verifier_detects_broken_chain(tmp_path):

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
        previous_hash="BROKEN_HASH",
        current_hash="hash-002",
    )

    verifier = HashChainVerifier(
        db_path
    )

    assert not verifier.verify()
