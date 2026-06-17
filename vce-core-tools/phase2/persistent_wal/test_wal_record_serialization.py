from phase2.persistent_wal.wal_schema import (
    WALRecord,
)


def test_record_serializes_to_dict():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001"
        },
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    result = record.to_dict()

    assert result["lsn"] == 1

    assert (
        result["opcode"]
        == "APPEND_EVENT"
    )


def test_serialized_record_contains_payload():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={
            "id": "event-001"
        },
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    result = record.to_dict()

    assert (
        result["payload"]["id"]
        == "event-001"
    )


def test_serialized_record_contains_hash_chain():

    record = WALRecord(
        lsn=1,
        opcode="APPEND_EVENT",
        payload={},
        previous_hash="GENESIS",
        current_hash="hash-001",
    )

    result = record.to_dict()

    assert (
        result["previous_hash"]
        == "GENESIS"
    )

    assert (
        result["current_hash"]
        == "hash-001"
    )
