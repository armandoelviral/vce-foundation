from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TransparencyEntryRecord:

    entry_id: str
    entry_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "entry_id": self.entry_id,
            "entry_hash": self.entry_hash,
        }
