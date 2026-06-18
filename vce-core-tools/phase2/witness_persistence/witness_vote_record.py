from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class WitnessVoteRecord:

    witness_id: str
    decision_id: str
    vote: bool

    def to_dict(self) -> Dict[str, Union[str, bool]]:

        return {
            "witness_id": self.witness_id,
            "decision_id": self.decision_id,
            "vote": self.vote,
        }
