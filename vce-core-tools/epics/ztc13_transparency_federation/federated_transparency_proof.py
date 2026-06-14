from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class FederatedTransparencyProof:

    anchor_id: str
    source_registry: str
    target_registry: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "anchor_id": self.anchor_id,
            "source_registry": self.source_registry,
            "target_registry": self.target_registry,
        }
