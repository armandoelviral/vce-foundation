from epics.phase8_006_historical_civilization_replay.civilization_replay_record import (
    CivilizationReplayRecord,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_registry import (
    CivilizationReplayRegistry,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_state import (
    CivilizationReplayState,
)
from epics.phase8_006_historical_civilization_replay.civilization_replay_verifier import (
    verify_civilization_replay,
)


def test_end_to_end_civilization_replay_flow():
    registry = CivilizationReplayRegistry()

    registry.add(
        CivilizationReplayRecord(
            "civ_replay.001",
            "snapshot.001",
            100,
        )
    )

    registry.add(
        CivilizationReplayRecord(
            "civ_replay.002",
            "snapshot.002",
            200,
        )
    )

    state = CivilizationReplayState.from_records(
        registry.records()
    )

    verification = verify_civilization_replay(state)

    assert verification["verified"] is True
    assert verification["latest_epoch"] == 200
