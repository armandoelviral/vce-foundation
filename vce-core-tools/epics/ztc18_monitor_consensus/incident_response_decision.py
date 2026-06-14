from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class IncidentResponseDecision:

    incident_id: str
    approved: bool

    def to_dict(self) -> Dict[str, bool]:

        return {
            "incident_id": self.incident_id,
            "approved": self.approved,
        }
