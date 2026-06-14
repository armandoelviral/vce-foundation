from dataclasses import dataclass
from typing import Dict

from epics.ztc9_supply_chain_provenance.source_provenance_record import (
    SourceProvenanceRecord,
)

from epics.ztc9_supply_chain_provenance.build_provenance_record import (
    BuildProvenanceRecord,
)

from epics.ztc9_supply_chain_provenance.artifact_provenance_record import (
    ArtifactProvenanceRecord,
)


@dataclass(frozen=True)
class ProvenanceChain:
    source: SourceProvenanceRecord
    build: BuildProvenanceRecord
    artifact: ArtifactProvenanceRecord

    def to_dict(self) -> Dict:
        return {
            "source": self.source.to_dict(),
            "build": self.build.to_dict(),
            "artifact": self.artifact.to_dict(),
        }
