from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationClaim:

    identity_id: str
    claim_type: str

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "claim_type": self.claim_type,
        }
