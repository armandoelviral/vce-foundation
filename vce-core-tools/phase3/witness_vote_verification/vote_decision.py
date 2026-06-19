from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class VoteDecision:

    status: str

    @staticmethod
    def from_verification(
        verification: bool,
    ):

        return VoteDecision(
            status=(
                "ACCEPT_VOTE"
                if verification
                else "REJECT_VOTE"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
