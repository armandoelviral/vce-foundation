from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ActivationAnchor:

    anchor_id: str
    rotation_id: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "anchor_id": self.anchor_id,
            "rotation_id": self.rotation_id,
        }
