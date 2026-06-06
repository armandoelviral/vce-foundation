from epics.epic043_snapshot_object.snapshot import Snapshot
from epics.epic044_snapshot_builder.snapshot_builder import SnapshotBuilder
from epics.epic045_snapshot_validator.snapshot_validator import (
    SnapshotValidator,
)


def test_validates_matching_snapshot():

    events = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    snapshot = SnapshotBuilder().build(events)

    validator = SnapshotValidator()

    assert validator.validate(events, snapshot) is True


def test_rejects_mismatching_snapshot():

    events = [
        {"sequence": 1, "event": "BOOTSTRAP"},
        {"sequence": 2, "event": "RECOVERED"},
        {"sequence": 3, "event": "RECOVERED"},
    ]

    bad_snapshot = Snapshot(
        sequence=3,
        state_hash="bad",
    )

    validator = SnapshotValidator()

    assert validator.validate(events, bad_snapshot) is False
