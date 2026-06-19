from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VersionApprovalDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return VersionApprovalDecision(
            status=(
                "APPROVE_VERSION"
                if evaluation
                else "REJECT_VERSION"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
