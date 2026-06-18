from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class EvidenceNode:

    node_id: str
    node_type: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
        }
