from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HistoricalReplayDecision:

    status: str

    @staticmethod
    def from_evaluation(
        evaluation: bool,
    ):

        return HistoricalReplayDecision(
            status=(
                "REPLAY"
                if evaluation
                else "REJECT_REPLAY"
            )
        )

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
