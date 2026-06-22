from dataclasses import dataclass


@dataclass(frozen=True)
class VoteRecord:

    citizen_did: str
    proposal_id: str
    vote: str

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "proposal_id":
                self.proposal_id,
            "vote":
                self.vote,
        }
