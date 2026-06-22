from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionAmendment:

    amendment_id: str
    proposal_id: str

    def to_dict(self):

        return {
            "amendment_id":
                self.amendment_id,
            "proposal_id":
                self.proposal_id,
        }
