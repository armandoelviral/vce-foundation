from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)
from epics.phase8_004_constitutional_snapshots.snapshot_registry import (
    SnapshotRegistry,
)
from epics.phase8_004_constitutional_snapshots.snapshot_restore import (
    restore_snapshot,
)
from epics.phase8_004_constitutional_snapshots.snapshot_state import (
    SnapshotState,
)
from epics.phase8_004_constitutional_snapshots.snapshot_verifier import (
    verify_snapshot_state,
)


def test_end_to_end_snapshot_flow():
    registry = SnapshotRegistry()

    registry.add(
        SnapshotRecord(
            "snapshot.001",
            "root.abc123",
            100,
        )
    )

    registry.add(
        SnapshotRecord(
            "snapshot.002",
            "root.def456",
            200,
        )
    )

    state = SnapshotState.from_records(
        registry.records()
    )

    verification = verify_snapshot_state(state)
    restored = restore_snapshot(
        registry.records()[-1]
    )

    assert verification["verified"] is True
    assert verification["latest_epoch"] == 200
    assert restored["restored"] is True
    assert restored["state_root"] == "root.def456"
