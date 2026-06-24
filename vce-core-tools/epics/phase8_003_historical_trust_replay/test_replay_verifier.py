from epics.phase8_003_historical_trust_replay.replay_state import (
    ReplayState,
)
from epics.phase8_003_historical_trust_replay.replay_verifier import (
    verify_replay,
)


def test_replay_verified():
    state = ReplayState(
        total_records=2,
        max_epoch=200,
    )

    result = verify_replay(state)

    assert result["verified"] is True


def test_empty_replay_not_verified():
    state = ReplayState(
        total_records=0,
        max_epoch=0,
    )

    result = verify_replay(state)

    assert result["verified"] is False
