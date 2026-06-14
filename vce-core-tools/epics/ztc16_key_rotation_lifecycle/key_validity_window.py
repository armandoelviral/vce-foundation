from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class KeyValidityWindow:

    key_id: str
    start_anchor: str
    end_anchor: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "key_id": self.key_id,
            "start_anchor": self.start_anchor,
            "end_anchor": self.end_anchor,
        }
