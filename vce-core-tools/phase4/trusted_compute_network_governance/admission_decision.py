from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionDecision:

    proposal_id: str
    approved: bool
    vote_count: int

    def to_dict(self):

        return {
            "proposal_id": self.proposal_id,
            "approved": self.approved,
            "vote_count": self.vote_count,
        }
