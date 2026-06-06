from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)
from epics.epic012_replay_runtime.snapshot_manager import (
    SnapshotManager,
)


@given(
    st.lists(
        st.text(
            min_size=1,
            max_size=50,
        ),
        min_size=1,
        max_size=25,
    )
)
def test_snapshot_preserves_runtime_state(events):

    engine = ReplayEngine()

    state = engine.replay(
        events
    )

    manager = SnapshotManager()

    snapshot = manager.seal(
        state,
        "/tmp/property_snapshot.json",
    )

    assert (
        snapshot["state_hash"]
        ==
        state.state_hash
    )

    assert (
        snapshot["event_count"]
        ==
        state.sequence_number
    )
