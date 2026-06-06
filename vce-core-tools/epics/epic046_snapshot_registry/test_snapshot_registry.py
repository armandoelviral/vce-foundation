from epics.epic043_snapshot_object.snapshot import Snapshot
from epics.epic046_snapshot_registry.snapshot_registry import (
    SnapshotRegistry,
)


def test_add_and_get_snapshot():

    registry = SnapshotRegistry()

    snapshot = Snapshot(
        sequence=42,
        state_hash="abc123",
    )

    registry.add(snapshot)

    assert registry.get(42) == snapshot


def test_latest_returns_highest_sequence():

    registry = SnapshotRegistry()

    registry.add(
        Snapshot(
            sequence=1,
            state_hash="a",
        )
    )

    registry.add(
        Snapshot(
            sequence=5,
            state_hash="b",
        )
    )

    registry.add(
        Snapshot(
            sequence=3,
            state_hash="c",
        )
    )

    latest = registry.latest()

    assert latest.sequence == 5
    assert latest.state_hash == "b"
