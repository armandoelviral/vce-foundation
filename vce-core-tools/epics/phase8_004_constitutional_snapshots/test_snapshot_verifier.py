from epics.phase8_004_constitutional_snapshots.snapshot_state import (
    SnapshotState,
)
from epics.phase8_004_constitutional_snapshots.snapshot_verifier import (
    verify_snapshot_state,
)


def test_snapshot_state_verified():
    state = SnapshotState(
        total_snapshots=2,
        latest_epoch=200,
    )

    result = verify_snapshot_state(state)

    assert result["verified"] is True


def test_empty_snapshot_state_not_verified():
    state = SnapshotState(
        total_snapshots=0,
        latest_epoch=0,
    )

    result = verify_snapshot_state(state)

    assert result["verified"] is False
