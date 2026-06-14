from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceEvent:
    event_id: str
    event_type: str
    payload_hash: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "payload_hash": self.payload_hash,
        }
