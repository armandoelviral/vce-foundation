from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)


def test_replay_record_creation():
    record = ReplayRecord(
        replay_id="replay.001",
        trust_id="trust.001",
        historical_epoch=100,
    )

    assert record.historical_epoch == 100


def test_requires_replay_id():
    try:
        ReplayRecord(
            "",
            "trust.001",
            100,
        )
        assert False
    except ValueError as exc:
        assert "replay_id" in str(exc)
