from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExecutionProvenanceBinding:

    execution_id: str
    provenance_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "execution_id": self.execution_id,
            "provenance_hash": self.provenance_hash,
        }
