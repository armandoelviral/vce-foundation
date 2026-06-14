from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class KeyRotationRecord:
    witness_id: str
    old_key_id: str
    new_key_id: str
    reason: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "witness_id": self.witness_id,
            "old_key_id": self.old_key_id,
            "new_key_id": self.new_key_id,
            "reason": self.reason,
        }
