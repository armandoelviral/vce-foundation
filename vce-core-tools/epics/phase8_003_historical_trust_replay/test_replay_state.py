from epics.phase8_003_historical_trust_replay.replay_record import (
    ReplayRecord,
)
from epics.phase8_003_historical_trust_replay.replay_state import (
    ReplayState,
)


def test_builds_replay_state():
    records = [
        ReplayRecord(
            "replay.001",
            "trust.001",
            100,
        ),
        ReplayRecord(
            "replay.002",
            "trust.002",
            200,
        ),
    ]

    state = ReplayState.from_records(records)

    assert state.total_records == 2
    assert state.max_epoch == 200


def test_empty_replay_state():
    state = ReplayState.from_records([])

    assert state.total_records == 0
    assert state.max_epoch == 0
