from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DeploymentManifest:

    release_id: str
    artifact_hash: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "release_id": self.release_id,
            "artifact_hash": self.artifact_hash,
        }
