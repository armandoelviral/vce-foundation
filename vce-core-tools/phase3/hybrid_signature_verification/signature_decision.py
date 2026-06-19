from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SignatureDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return SignatureDecision(
            status=(
                "ACCEPT_SIGNATURE"
                if evaluation
                else "REJECT_SIGNATURE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status":
                self.status
        }
