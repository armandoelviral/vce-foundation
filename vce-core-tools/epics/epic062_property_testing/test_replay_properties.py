from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)


@given(
    st.lists(
        st.text(
            min_size=1,
            max_size=50,
        ),
        min_size=0,
        max_size=25,
    )
)
def test_replay_is_deterministic_for_any_event_list(events):

    engine = ReplayEngine()

    state_a = engine.replay(events)
    state_b = engine.replay(events)

    assert state_a.state_hash == state_b.state_hash
    assert state_a.sequence_number == state_b.sequence_number
