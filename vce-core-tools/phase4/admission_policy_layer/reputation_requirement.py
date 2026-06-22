from dataclasses import dataclass


@dataclass(frozen=True)
class ReputationRequirement:

    minimum_score: int

    def is_satisfied(
        self,
        reputation_score: int,
    ) -> bool:

        return reputation_score >= self.minimum_score

    def to_dict(self):

        return {
            "requirement_type": "REPUTATION",
            "minimum_score": self.minimum_score,
        }
