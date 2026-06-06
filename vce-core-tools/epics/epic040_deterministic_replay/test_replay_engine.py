from epics.epic041_runtime_state.runtime_state import (
    RuntimeState,
)
from epics.epic040_deterministic_replay.replay_engine import (
    ReplayEngine,
)


def test_same_log_produces_same_state():

    events = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    replay_a = ReplayEngine()
    replay_b = ReplayEngine()

    state_a = replay_a.replay(events)
    state_b = replay_b.replay(events)

    assert state_a == state_b

def test_different_log_produces_different_state():

    events_a = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
    ]

    events_b = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    replay = ReplayEngine()

    assert replay.replay(events_a) != replay.replay(events_b)
