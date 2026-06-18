from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class WitnessReplayBinding:

    decision_id: str
    replay_lsn: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "decision_id": self.decision_id,
            "replay_lsn": self.replay_lsn,
        }
