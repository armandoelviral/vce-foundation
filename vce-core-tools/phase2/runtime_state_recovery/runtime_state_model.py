from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class RuntimeState:

    events_applied: int = 0
    last_lsn: int = 0
    state_hash: str = "GENESIS"

    def to_dict(
        self,
    ) -> Dict[str, Union[int, str]]:

        return {
            "events_applied": self.events_applied,
            "last_lsn": self.last_lsn,
            "state_hash": self.state_hash,
        }
