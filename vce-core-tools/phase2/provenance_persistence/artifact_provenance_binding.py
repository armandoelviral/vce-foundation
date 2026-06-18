from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ArtifactProvenanceBinding:

    artifact_id: str
    provenance_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "artifact_id": self.artifact_id,
            "provenance_hash": self.provenance_hash,
        }
