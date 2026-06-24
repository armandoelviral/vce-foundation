from epics.phase8_006_historical_civilization_replay.civilization_replay_plan import (
    civilization_replay_requested,
)


def test_civilization_replay_requested():
    assert civilization_replay_requested(100) is True


def test_invalid_civilization_replay_request():
    assert civilization_replay_requested(0) is False
