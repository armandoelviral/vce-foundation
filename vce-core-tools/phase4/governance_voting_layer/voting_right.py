from dataclasses import dataclass


@dataclass(frozen=True)
class VotingRight:

    citizen_did: str
    voting_right: bool

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "voting_right":
                self.voting_right,
        }
