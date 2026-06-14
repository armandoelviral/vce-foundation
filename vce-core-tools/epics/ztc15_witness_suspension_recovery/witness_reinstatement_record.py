from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessReinstatementRecord:
    witness_id: str
    reinstatement_reason: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "witness_id": self.witness_id,
            "reinstatement_reason": self.reinstatement_reason,
        }
