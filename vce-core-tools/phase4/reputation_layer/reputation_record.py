from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationRecord:

    citizen_did: str
    reputation_score: int

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "reputation_score":
                self.reputation_score,
        }
