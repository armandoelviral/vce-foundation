from dataclasses import dataclass


@dataclass(frozen=True)
class GovernanceProposal:

    proposal_id: str
    title: str

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "title":
                self.title,
        }
