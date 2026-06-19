from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class InclusionProofRecord:

    leaf_id: str
    root_id: str
    proof_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "leaf_id": self.leaf_id,
            "root_id": self.root_id,
            "proof_hash": self.proof_hash,
        }
