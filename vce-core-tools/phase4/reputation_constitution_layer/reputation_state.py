from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationState:

    score: int

    def to_dict(self):

        return {
            "score": self.score,
        }
