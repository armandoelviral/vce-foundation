from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DelegationDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return DelegationDecision(
            status=(
                "DELEGATE"
                if evaluation
                else "DENY"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
