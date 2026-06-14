from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class CrossAnchorRecord:
    source_registry: str
    target_registry: str
    source_anchor_id: str
    target_anchor_id: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "source_registry": self.source_registry,
            "target_registry": self.target_registry,
            "source_anchor_id": self.source_anchor_id,
            "target_anchor_id": self.target_anchor_id,
        }
