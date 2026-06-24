from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)
from epics.phase8_004_constitutional_snapshots.snapshot_restore import (
    restore_snapshot,
)


def test_restores_snapshot():
    snapshot = SnapshotRecord(
        "snapshot.001",
        "root.abc123",
        100,
    )

    restored = restore_snapshot(snapshot)

    assert restored["restored"] is True
    assert restored["state_root"] == "root.abc123"


def test_restore_reports_epoch():
    snapshot = SnapshotRecord(
        "snapshot.001",
        "root.abc123",
        100,
    )

    restored = restore_snapshot(snapshot)

    assert restored["epoch"] == 100
