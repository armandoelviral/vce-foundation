from epics.epic089_replay_transparency_log.replay_log_record import (
    ReplayLogRecord,
)


def test_log_record_contains_chain_fields():
    record = ReplayLogRecord(
        sequence=1,
        previous_hash="GENESIS",
        current_hash="hash-001",
        replay_id="replay-001",
    )

    assert record.sequence == 1
    assert record.previous_hash == "GENESIS"
    assert record.current_hash == "hash-001"
    assert record.replay_id == "replay-001"


def test_log_record_serializes():
    record = ReplayLogRecord(
        sequence=1,
        previous_hash="GENESIS",
        current_hash="hash-001",
        replay_id="replay-001",
    )

    assert record.to_dict() == {
        "sequence": 1,
        "previous_hash": "GENESIS",
        "current_hash": "hash-001",
        "replay_id": "replay-001",
    }
