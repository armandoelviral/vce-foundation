from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessSuspensionRecord:

    witness_id: str
    reason: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "witness_id": self.witness_id,
            "reason": self.reason,
        }
