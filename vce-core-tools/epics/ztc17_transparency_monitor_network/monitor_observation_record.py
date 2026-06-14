from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class MonitorObservationRecord:
    monitor_id: str
    registry_id: str
    observed_root: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "monitor_id": self.monitor_id,
            "registry_id": self.registry_id,
            "observed_root": self.observed_root,
        }
