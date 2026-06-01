import os

from epics.epic022_persistence.snapshot_manager import (
    SnapshotManager
)


snapshot = SnapshotManager()

path = "runtime_snapshot.json"

state = {
    "sequence_number": 42,
    "state_hash": "abc123",
    "trust": "ACCEPTED"
}


snapshot.save(
    path,
    state
)


loaded = snapshot.load(
    path
)


print(
    loaded["sequence_number"]
)

print(
    loaded["state_hash"]
)

print(
    loaded["trust"]
)


if os.path.exists(path):
    os.remove(path)
