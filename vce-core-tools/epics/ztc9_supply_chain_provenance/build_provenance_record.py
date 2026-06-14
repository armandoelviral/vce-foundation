from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class BuildProvenanceRecord:
    build_id: str
    builder: str
    workflow: str
    source_commit: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "build_id": self.build_id,
            "builder": self.builder,
            "workflow": self.workflow,
            "source_commit": self.source_commit,
        }
