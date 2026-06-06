from epics.epic040_deterministic_replay.replay_engine import (
    ReplayEngine,
)

from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)

def test_runtime_state_tracks_event_count_and_last_sequence():

    state = RuntimeState(
        event_count=3,
        last_sequence=3,
    )

    assert state.event_count == 3
    assert state.last_sequence == 3

def test_replay_returns_runtime_state():

    events = [
        {"sequence": 1},
        {"sequence": 2},
        {"sequence": 3},
    ]

    replay = ReplayEngine()

    state = replay.replay(events)

    assert isinstance(
        state,
        RuntimeState,
    )

