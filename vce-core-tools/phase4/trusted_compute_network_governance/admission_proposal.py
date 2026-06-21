from dataclasses import dataclass


@dataclass(frozen=True)
class AdmissionProposal:

    proposal_id: str
    candidate_did: str
    sponsor_did: str

    @property
    def proposal_type(self):

        return "ADMISSION"

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "candidate_did":
                self.candidate_did,
            "sponsor_did":
                self.sponsor_did,
            "proposal_type":
                self.proposal_type,
        }
