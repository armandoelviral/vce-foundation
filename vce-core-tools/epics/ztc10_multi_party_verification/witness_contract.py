from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessContract:
    witness_id: str
    public_key: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "witness_id": self.witness_id,
            "public_key": self.public_key,
        }
