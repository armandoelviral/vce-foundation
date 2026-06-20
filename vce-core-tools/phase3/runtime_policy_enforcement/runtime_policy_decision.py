from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RuntimePolicyDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return RuntimePolicyDecision(
            status=(
                "ALLOW_REQUEST"
                if evaluation
                else "DENY_REQUEST"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status":
                self.status
        }
