from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)
from epics.phase8_004_constitutional_snapshots.snapshot_state import (
    SnapshotState,
)


def test_builds_snapshot_state():
    records = [
        SnapshotRecord("snapshot.001", "root.abc123", 100),
        SnapshotRecord("snapshot.002", "root.def456", 200),
    ]

    state = SnapshotState.from_records(records)

    assert state.total_snapshots == 2
    assert state.latest_epoch == 200


def test_empty_snapshot_state():
    state = SnapshotState.from_records([])

    assert state.total_snapshots == 0
    assert state.latest_epoch == 0
