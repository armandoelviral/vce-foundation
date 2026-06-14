from dataclasses import dataclass
from typing import Dict

from epics.ztc11_distributed_attestation.attestation_anchor import (
    AttestationAnchor,
)


@dataclass(frozen=True)
class AttestationReplica:
    replica_id: str
    anchor: AttestationAnchor
    location: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "replica_id": self.replica_id,
            "anchor_id": self.anchor.anchor_id,
            "location": self.location,
        }
