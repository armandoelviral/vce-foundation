from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class LineageDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return LineageDecision(
            status=(
                "ACCEPT_LINEAGE"
                if evaluation
                else "REJECT_LINEAGE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
