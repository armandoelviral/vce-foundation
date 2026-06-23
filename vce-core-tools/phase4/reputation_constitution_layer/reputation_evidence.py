from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationEvidence:

    claim_id: str
    evidence_hash: str

    def to_dict(self):

        return {
            "claim_id": self.claim_id,
            "evidence_hash": self.evidence_hash,
        }
