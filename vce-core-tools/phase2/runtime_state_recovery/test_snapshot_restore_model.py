from phase2.runtime_state_recovery.snapshot_restore_model import (
    SnapshotRestoreModel,
)

from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


def test_restore_snapshot_returns_state():

    snapshot = SnapshotRestoreModel(
        lsn=100,
        events_applied=100,
        state_hash="state-001",
    )

    state = snapshot.restore()

    assert isinstance(
        state,
        RuntimeState,
    )


def test_restore_preserves_lsn():

    snapshot = SnapshotRestoreModel(
        lsn=100,
        events_applied=100,
        state_hash="state-001",
    )

    state = snapshot.restore()

    assert state.last_lsn == 100


def test_restore_preserves_hash():

    snapshot = SnapshotRestoreModel(
        lsn=100,
        events_applied=100,
        state_hash="state-001",
    )

    state = snapshot.restore()

    assert (
        state.state_hash
        == "state-001"
    )
