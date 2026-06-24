from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_state import (
    CivilizationReplayState,
)


def test_builds_civilization_replay_state():
    records = [
        CivilizationReplayRecord(
            "civ_replay.001",
            "snapshot.001",
            100,
        ),
        CivilizationReplayRecord(
            "civ_replay.002",
            "snapshot.002",
            200,
        ),
    ]

    state = CivilizationReplayState.from_records(records)

    assert state.total_records == 2
    assert state.latest_epoch == 200


def test_empty_civilization_replay_state():
    state = CivilizationReplayState.from_records([])

    assert state.total_records == 0
    assert state.latest_epoch == 0
