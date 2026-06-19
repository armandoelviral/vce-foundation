from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RecoveryRecord:

    recovery_id: str
    incident_id: str
    recovery_reason: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "recovery_id":
                self.recovery_id,
            "incident_id":
                self.incident_id,
            "recovery_reason":
                self.recovery_reason,
        }
