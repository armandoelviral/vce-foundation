from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class KeySlot:

    name: str
    key_id: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "name": self.name,
            "key_id": self.key_id,
        }
