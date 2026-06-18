from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class ExecutionReplayBinding:

    execution_id: str
    replay_lsn: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "execution_id": self.execution_id,
            "replay_lsn": self.replay_lsn,
        }
