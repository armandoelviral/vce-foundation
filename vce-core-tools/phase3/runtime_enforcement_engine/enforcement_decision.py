from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class EnforcementDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: str,
    ):

        return EnforcementDecision(
            status=evaluation
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
