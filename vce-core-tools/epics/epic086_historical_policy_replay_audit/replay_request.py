from dataclasses import dataclass


@dataclass(frozen=True)
class ReplayRequest:
    evidence_hash: str
    policy_id: str
    policy_version: str
    requested_by: str
    requested_at: str

    def to_dict(self):

        return {
            "evidence_hash": self.evidence_hash,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at,
        }
