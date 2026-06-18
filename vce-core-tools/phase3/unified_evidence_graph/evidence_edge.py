from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class EvidenceEdge:

    source_id: str
    target_id: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
        }
