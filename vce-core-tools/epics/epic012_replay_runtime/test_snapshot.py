from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)
from epics.epic012_replay_runtime.snapshot_manager import (
    SnapshotManager,
)


def test_snapshot_contains_state_hash():

    engine = ReplayEngine()

    state = engine.replay(
        [
            "APPEND_EVIDENCE",
            "REGISTER_ARTIFACT",
            "SEAL_SNAPSHOT",
        ]
    )

    manager = SnapshotManager()

    snapshot = manager.seal(
        state,
        "epics/epic012_replay_runtime/snapshot.json",
    )

    assert "state_hash" in snapshot


def test_snapshot_records_event_count():

    engine = ReplayEngine()

    state = engine.replay(
        [
            "APPEND_EVIDENCE",
            "REGISTER_ARTIFACT",
            "SEAL_SNAPSHOT",
        ]
    )

    manager = SnapshotManager()

    snapshot = manager.seal(
        state,
        "epics/epic012_replay_runtime/snapshot.json",
    )

    assert snapshot["event_count"] == 3
