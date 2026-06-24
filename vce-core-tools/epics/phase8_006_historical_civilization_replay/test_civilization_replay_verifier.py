from epics.phase8_006_historical_civilization_replay.civilization_replay_state import (
    CivilizationReplayState,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_verifier import (
    verify_civilization_replay,
)


def test_civilization_replay_verified():
    state = CivilizationReplayState(
        total_records=2,
        latest_epoch=200,
    )

    result = verify_civilization_replay(state)

    assert result["verified"] is True


def test_empty_civilization_replay_not_verified():
    state = CivilizationReplayState(
        total_records=0,
        latest_epoch=0,
    )

    result = verify_civilization_replay(state)

    assert result["verified"] is False
