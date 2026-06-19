from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return GovernanceDecision(
            status=(
                "APPROVED"
                if evaluation
                else "REJECTED"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
