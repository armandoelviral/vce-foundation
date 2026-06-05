from epics.epic029_majority_commit.commit_coordinator import (
    CommitCoordinator
)

coordinator = CommitCoordinator()

result = coordinator.commit(
    [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002"
    ],
    {
        "sequence": 200,
        "event": "MAJORITY_COMMIT_TEST"
    }
)

print(result)
