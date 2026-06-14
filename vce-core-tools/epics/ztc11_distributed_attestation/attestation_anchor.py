from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AttestationAnchor:
    anchor_id: str
    attestation_hash: str
    state_root_hash: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "anchor_id": self.anchor_id,
            "attestation_hash": self.attestation_hash,
            "state_root_hash": self.state_root_hash,
        }
