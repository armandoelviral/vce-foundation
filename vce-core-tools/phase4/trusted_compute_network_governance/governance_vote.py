from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceVote:

    proposal_id: str
    tcu_did: str
    vote: str

    def to_dict(self):

        return {
            "proposal_id": self.proposal_id,
            "tcu_did": self.tcu_did,
            "vote": self.vote,
        }
