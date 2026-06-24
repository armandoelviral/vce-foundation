from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)


def test_snapshot_record_creation():
    record = SnapshotRecord(
        snapshot_id="snapshot.001",
        state_root="root.abc123",
        epoch=100,
    )

    assert record.snapshot_id == "snapshot.001"
    assert record.state_root == "root.abc123"
    assert record.epoch == 100


def test_requires_snapshot_id():
    try:
        SnapshotRecord("", "root.abc123", 100)
        assert False
    except ValueError as exc:
        assert "snapshot_id" in str(exc)
