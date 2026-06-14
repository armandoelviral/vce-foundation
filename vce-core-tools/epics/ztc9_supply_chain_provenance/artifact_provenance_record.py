from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ArtifactProvenanceRecord:
    artifact_id: str
    artifact_hash: str
    build_id: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_hash": self.artifact_hash,
            "build_id": self.build_id,
        }
