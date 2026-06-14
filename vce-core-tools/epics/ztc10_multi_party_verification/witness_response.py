from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessResponse:
    witness_id: str
    state_root_hash: str
    classical_signature: str
    pqc_signature: str
    accepted: bool

    def to_dict(self) -> Dict:
        return {
            "witness_id": self.witness_id,
            "state_root_hash": self.state_root_hash,
            "classical_signature": self.classical_signature,
            "pqc_signature": self.pqc_signature,
            "accepted": self.accepted,
        }
