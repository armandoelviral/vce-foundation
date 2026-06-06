from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)


@given(
    st.lists(
        st.text(min_size=1, max_size=30),
        min_size=1,
        max_size=20,
    )
)
def test_same_input_same_hash(events):

    engine = ReplayEngine()

    state_a = engine.replay(events)
    state_b = engine.replay(events)

    assert state_a.state_hash == state_b.state_hash


@given(
    st.lists(
        st.text(min_size=1, max_size=30),
        min_size=2,
        max_size=20,
    )
)
def test_order_change_changes_hash(events):

    engine = ReplayEngine()

    original = engine.replay(events)

    modified = events.copy()
    modified.reverse()

    reversed_state = engine.replay(modified)

    if events != modified:
        assert (
            original.state_hash
            != reversed_state.state_hash
        )
