from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RootDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return RootDecision(
            status=(
                "ACCEPT_ROOT"
                if evaluation
                else "REJECT_ROOT"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
