from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ExecutionProvenanceRecord:
    artifact_hash: str
    execution_id: str
    result_hash: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "artifact_hash": self.artifact_hash,
            "execution_id": self.execution_id,
            "result_hash": self.result_hash,
        }
