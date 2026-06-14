from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WasmArtifactIdentity:
    artifact_id: str
    module_name: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "module_name": self.module_name,
        }
