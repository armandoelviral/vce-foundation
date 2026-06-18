from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)


def test_record_contains_replay_id():

    record = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    assert record.replay_id == "replay-001"


def test_record_contains_bundle_id():

    record = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    assert record.bundle_id == "bundle-001"


def test_record_serializes():

    record = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    assert record.to_dict() == {
        "replay_id": "replay-001",
        "bundle_id": "bundle-001",
    }
