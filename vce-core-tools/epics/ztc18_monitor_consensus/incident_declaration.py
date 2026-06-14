from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class IncidentDeclaration:
    incident_id: str
    reason: str
    declared: bool

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        return {
            "incident_id": self.incident_id,
            "reason": self.reason,
            "declared": self.declared,
        }
