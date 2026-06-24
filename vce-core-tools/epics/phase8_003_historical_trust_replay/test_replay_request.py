from epics.phase8_003_historical_trust_replay.replay_request import (
    replay_requested,
)


def test_replay_requested():
    assert replay_requested(100) is True


def test_invalid_replay_request():
    assert replay_requested(0) is False
