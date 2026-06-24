from epics.phase8_004_constitutional_snapshots.snapshot_record import (
    SnapshotRecord,
)


def restore_snapshot(snapshot: SnapshotRecord):
    return {
        "restored": True,
        "snapshot_id": snapshot.snapshot_id,
        "state_root": snapshot.state_root,
        "epoch": snapshot.epoch,
    }
