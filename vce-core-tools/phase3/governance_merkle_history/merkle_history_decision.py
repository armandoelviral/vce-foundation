from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MerkleHistoryDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return MerkleHistoryDecision(
            status=(
                "ACCEPT_MERKLE"
                if evaluation
                else "REJECT_MERKLE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
