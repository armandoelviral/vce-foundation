from epics.epic043_snapshot_object.snapshot import Snapshot
from epics.epic044_snapshot_builder.snapshot_builder import SnapshotBuilder


def test_builds_snapshot_from_events():

    events = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    builder = SnapshotBuilder()

    snapshot = builder.build(events)

    assert isinstance(snapshot, Snapshot)
    assert snapshot.sequence == 3
    assert isinstance(snapshot.state_hash, str)
    assert len(snapshot.state_hash) == 64
