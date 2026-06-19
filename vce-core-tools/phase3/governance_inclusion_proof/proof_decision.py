from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProofDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return ProofDecision(
            status=(
                "ACCEPT_PROOF"
                if evaluation
                else "REJECT_PROOF"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
