from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceMerkleRootRecord:

    root_id: str
    root_hash: str
    leaf_count: int

    def to_dict(
        self,
    ) -> Dict:

        return {
            "root_id": self.root_id,
            "root_hash": self.root_hash,
            "leaf_count": self.leaf_count,
        }
