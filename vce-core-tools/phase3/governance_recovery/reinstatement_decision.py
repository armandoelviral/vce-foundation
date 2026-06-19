from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReinstatementDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return ReinstatementDecision(
            status=(
                "REINSTATE"
                if evaluation
                else "REJECT_REINSTATEMENT"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
