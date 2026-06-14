from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MonitorAlertRecord:
    monitor_id: str
    registry_id: str
    reason: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "monitor_id": self.monitor_id,
            "registry_id": self.registry_id,
            "reason": self.reason,
        }
