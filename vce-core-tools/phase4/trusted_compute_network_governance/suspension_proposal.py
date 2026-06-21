from dataclasses import dataclass


@dataclass(frozen=True)
class SuspensionProposal:

    proposal_id: str
    target_did: str
    sponsor_did: str
    reason: str

    @property
    def proposal_type(self):

        return "SUSPENSION"

    def to_dict(self):

        return {
            "proposal_id":
                self.proposal_id,
            "target_did":
                self.target_did,
            "sponsor_did":
                self.sponsor_did,
            "reason":
                self.reason,
            "proposal_type":
                self.proposal_type,
        }
