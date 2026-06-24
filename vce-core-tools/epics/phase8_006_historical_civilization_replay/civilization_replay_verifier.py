from epics.phase8_006_historical_civilization_replay.civilization_replay_state import (
    CivilizationReplayState,
)


def verify_civilization_replay(
    state: CivilizationReplayState,
):
    return {
        "verified": state.latest_epoch > 0,
        "latest_epoch": state.latest_epoch,
        "total_records": state.total_records,
    }
