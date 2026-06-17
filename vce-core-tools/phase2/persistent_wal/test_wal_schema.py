from phase2.persistent_wal.wal_schema import (
    WALRecord,
)


def test_record_contains_lsn():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    assert record.lsn == 1


def test_record_contains_opcode():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    assert (
        record.opcode
        == "APPEND_EVENT"
    )


def test_record_contains_hash_chain():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={"id": "event-001"},
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    assert (
        record.previous_hash
        == "GENESIS"
    )

    assert (
        record.current_hash
        == "hash-001"
    )
