from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class EscalationRecord:

    escalation_id: str
    reason: str
    severity: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "escalation_id":
                self.escalation_id,
            "reason":
                self.reason,
            "severity":
                self.severity,
        }
