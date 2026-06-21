from dataclasses import dataclass


@dataclass(frozen=True)
class ReinstatementProposal:

    proposal_id: str
    target_did: str
    sponsor_did: str
    evidence: str

    @property
    def proposal_type(self):

        return "REINSTATEMENT"

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "target_did":
                self.target_did,
            "sponsor_did":
                self.sponsor_did,
            "evidence":
                self.evidence,
            "proposal_type":
                self.proposal_type,
        }
