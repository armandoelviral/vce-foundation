from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)


def test_civilization_replay_record_creation():
    record = CivilizationReplayRecord(
        replay_id="civ_replay.001",
        snapshot_id="snapshot.001",
        epoch=100,
    )

    assert record.replay_id == "civ_replay.001"
    assert record.snapshot_id == "snapshot.001"
    assert record.epoch == 100


def test_requires_replay_id():
    try:
        CivilizationReplayRecord("", "snapshot.001", 100)
        assert False
    except ValueError as exc:
        assert "replay_id" in str(exc)
