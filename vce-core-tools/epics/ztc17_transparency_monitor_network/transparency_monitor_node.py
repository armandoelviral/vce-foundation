from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class TransparencyMonitorNode:
    monitor_id: str
    endpoint: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "monitor_id": self.monitor_id,
            "endpoint": self.endpoint,
        }
