from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)


@given(
    st.lists(
        st.text(),
        min_size=0,
        max_size=100,
    )
)
def test_replay_engine_never_crashes(events):

    engine = ReplayEngine()

    state = engine.replay(events)

    assert state is not None
