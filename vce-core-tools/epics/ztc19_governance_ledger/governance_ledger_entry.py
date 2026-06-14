from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class GovernanceLedgerEntry:

    sequence: int
    event_id: str

    def to_dict(
        self,
    ) -> Dict[str, Union[int, str]]:

        return {
            "sequence": self.sequence,
            "event_id": self.event_id,
        }
