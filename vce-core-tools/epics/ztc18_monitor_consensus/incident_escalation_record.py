from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class IncidentEscalationRecord:
    incident_id: str
    action: str
    target: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "incident_id": self.incident_id,
            "action": self.action,
            "target": self.target,
        }
