from epics.epic020_byzantine_fault_tolerance.conflict_detector import (
    ConflictDetector
)


detector = ConflictDetector()


vote1 = {
    "node_id": "node-X",
    "artifact_hash": "abc123",
    "decision": "APPROVE"
}


vote2 = {
    "node_id": "node-X",
    "artifact_hash": "abc123",
    "decision": "REJECT"
}


print(
    detector.observe(
        vote1
    )["conflict"]
)


print(
    detector.observe(
        vote2
    )["conflict"]
)
