from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RecoveryRecord:

    witness_id: str
    recovery_reason: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "witness_id": self.witness_id,
            "recovery_reason": self.recovery_reason,
        }
