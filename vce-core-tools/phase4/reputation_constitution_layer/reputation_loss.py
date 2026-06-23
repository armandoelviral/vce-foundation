from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationLoss:

    identity_id: str
    points: int

    def to_dict(self):

        return {
            "identity_id": self.identity_id,
            "points": self.points,
        }
