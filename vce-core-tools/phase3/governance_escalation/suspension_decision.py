from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SuspensionDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return SuspensionDecision(
            status=(
                "SUSPEND"
                if evaluation
                else "CONTINUE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
