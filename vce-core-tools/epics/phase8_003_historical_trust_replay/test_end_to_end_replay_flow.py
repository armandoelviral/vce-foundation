from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)
from epics.phase8_003_historical_trust_replay.replay_registry import (
    ReplayRegistry,
)
from epics.phase8_003_historical_trust_replay.replay_state import (
    ReplayState,
)
from epics.phase8_003_historical_trust_replay.replay_verifier import (
    verify_replay,
)


def test_end_to_end_replay_flow():
    registry = ReplayRegistry()

    registry.add(
        ReplayRecord(
            "replay.001",
            "trust.001",
            100,
        )
    )

    registry.add(
        ReplayRecord(
            "replay.002",
            "trust.002",
            200,
        )
    )

    state = ReplayState.from_records(
        registry.records()
    )

    verification = verify_replay(state)

    assert verification["verified"] is True
    assert verification["max_epoch"] == 200
