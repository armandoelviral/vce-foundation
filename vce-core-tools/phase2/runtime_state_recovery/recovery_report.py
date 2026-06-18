from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RecoveryReport:

    recovery_id: str
    recovered: bool
    state_hash_valid: bool

    def to_dict(self) -> Dict[str, bool | str]:

        return {
            "recovery_id": self.recovery_id,
            "recovered": self.recovered,
            "state_hash_valid": self.state_hash_valid,
        }
