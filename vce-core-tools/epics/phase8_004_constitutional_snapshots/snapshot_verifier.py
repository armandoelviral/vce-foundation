from epics.phase8_004_constitutional_snapshots.snapshot_state import (
    SnapshotState,
)


def verify_snapshot_state(state: SnapshotState):
    return {
        "verified": state.total_snapshots > 0 and state.latest_epoch > 0,
        "total_snapshots": state.total_snapshots,
        "latest_epoch": state.latest_epoch,
    }
