from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)
from epics.phase8_004_constitutional_snapshots.snapshot_registry import (
    SnapshotRegistry,
)


def test_registry_adds_snapshot():
    registry = SnapshotRegistry()

    record = SnapshotRecord(
        "snapshot.001",
        "root.abc123",
        100,
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_returns_copy():
    registry = SnapshotRegistry()

    registry.add(
        SnapshotRecord(
            "snapshot.001",
            "root.abc123",
            100,
        )
    )

    records = registry.records()
    records.clear()

    assert len(registry.records()) == 1
