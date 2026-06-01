from epics.epic020_byzantine_fault_tolerance.conflict_detector import (
    ConflictDetector
)

from epics.epic020_byzantine_fault_tolerance.byzantine_quorum import (
    ByzantineQuorum
)


class AdversarialConsensusTest:

    def run(self):

        detector = ConflictDetector()
        quorum = ByzantineQuorum()

        votes = [
            {
                "node_id": "node-A",
                "artifact_hash": "artifact-001",
                "decision": "APPROVE"
            },
            {
                "node_id": "node-B",
                "artifact_hash": "artifact-001",
                "decision": "APPROVE"
            },
            {
                "node_id": "node-C",
                "artifact_hash": "artifact-001",
                "decision": "APPROVE"
            }
        ]

        malicious_vote = {
            "node_id": "node-X",
            "artifact_hash": "artifact-001",
            "decision": "REJECT"
        }

        conflict = detector.observe(
            malicious_vote
        )

        approvals = sum(
            1
            for vote in votes
            if vote["decision"] == "APPROVE"
        )

        consensus = quorum.validate(
            total_validators=4,
            approvals=approvals
        )

        return {
            "conflict_detected":
                conflict["conflict"],

            "consensus":
                consensus["consensus"],

            "faults_tolerated":
                consensus["faults_tolerated"]
        }
