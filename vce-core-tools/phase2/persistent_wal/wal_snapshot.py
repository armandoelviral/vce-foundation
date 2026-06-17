from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class WALSnapshot:

    lsn: int
    state_hash: str

    def to_dict(
        self,
    ) -> Dict[str, Union[int, str]]:

        return {
            "lsn": self.lsn,
            "state_hash": self.state_hash,
        }
