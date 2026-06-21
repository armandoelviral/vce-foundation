from dataclasses import dataclass


@dataclass(frozen=True)
class SuspensionDecision:

    proposal_id: str
    target_did: str
    approved: bool
    vote_count: int

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "target_did":
                self.target_did,
            "approved":
                self.approved,
            "vote_count":
                self.vote_count,
        }
