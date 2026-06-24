from epics.phase8_003_historical_trust_replay.replay_state import (
    ReplayState,
)


def verify_replay(
    state: ReplayState,
):
    return {
        "verified": state.max_epoch > 0,
        "max_epoch": state.max_epoch,
        "total_records": state.total_records,
    }
