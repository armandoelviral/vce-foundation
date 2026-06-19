from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceMerkleLeaf:

    leaf_id: str
    snapshot_id: str
    hash_value: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "leaf_id": self.leaf_id,
            "snapshot_id": self.snapshot_id,
            "hash_value": self.hash_value,
        }
