from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationPenalty:

    citizen_did: str
    penalty_reason: str
    penalty_points: int

    def to_dict(self):

        return {
            "citizen_did":
                self.citizen_did,
            "penalty_reason":
                self.penalty_reason,
            "penalty_points":
                self.penalty_points,
        }
