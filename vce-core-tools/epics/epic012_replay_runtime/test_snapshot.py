from replay_engine import ReplayEngine
from snapshot_manager import SnapshotManager

engine = ReplayEngine()

events = [
    "APPEND_EVIDENCE",
    "REGISTER_ARTIFACT",
    "SEAL_SNAPSHOT"
]

state = engine.replay(
    events
)

manager = SnapshotManager()

snapshot = manager.seal(
    state,
    "epics/epic012_replay_runtime/snapshot.json"
)

print(
    snapshot["state_hash"]
)

print(
    snapshot["event_count"]
)
