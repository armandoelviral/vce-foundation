from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class TransparencyReplayBinding:

    root_hash: str
    replay_lsn: int

    def to_dict(
        self,
    ) -> Dict[str, Union[str, int]]:

        return {
            "root_hash": self.root_hash,
            "replay_lsn": self.replay_lsn,
        }
