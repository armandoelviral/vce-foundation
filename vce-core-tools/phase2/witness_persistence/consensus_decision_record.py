from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class ConsensusDecisionRecord:

    decision_id: str
    approved: bool
    vote_count: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool, int]]:

        return {
            "decision_id": self.decision_id,
            "approved": self.approved,
            "vote_count": self.vote_count,
        }
