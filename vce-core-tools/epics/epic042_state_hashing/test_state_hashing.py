from epics.epic041_runtime_state.runtime_state import RuntimeState
from epics.epic042_state_hashing.state_hasher import StateHasher


def test_same_state_produces_same_hash():

    state_a = RuntimeState(
        event_count=4,
        last_sequence=4,
    )

    state_b = RuntimeState(
        event_count=4,
        last_sequence=4,
    )

    hasher = StateHasher()

    assert hasher.hash(state_a) == hasher.hash(state_b)


def test_different_state_produces_different_hash():

    state_a = RuntimeState(
        event_count=4,
        last_sequence=4,
    )

    state_b = RuntimeState(
        event_count=5,
        last_sequence=5,
    )

    hasher = StateHasher()

    assert hasher.hash(state_a) != hasher.hash(state_b)
