from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationScore:

    citizen_did: str
    score: int

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "score":
                self.score,
        }
