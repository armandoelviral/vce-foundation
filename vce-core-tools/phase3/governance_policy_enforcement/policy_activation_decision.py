from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class PolicyActivationDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return PolicyActivationDecision(
            status=(
                "ACTIVATE_POLICY"
                if evaluation
                else "DO_NOT_ACTIVATE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status":
                self.status
        }
