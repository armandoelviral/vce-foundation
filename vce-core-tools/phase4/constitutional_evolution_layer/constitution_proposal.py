from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionProposal:

    proposal_id: str
    title: str
    status: str

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "title":
                self.title,
            "status":
                self.status,
        }
