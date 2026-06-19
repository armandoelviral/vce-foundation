from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TrustDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return TrustDecision(
            status=(
                "TRUSTED"
                if evaluation
                else "UNTRUSTED"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
