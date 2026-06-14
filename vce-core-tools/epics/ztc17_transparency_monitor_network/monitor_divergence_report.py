from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class MonitorDivergenceReport:
    monitor_a: str
    monitor_b: str
    registry_id: str
    divergent: bool

    def to_dict(self) -> Dict[str, Union[str, bool]]:
        return {
            "monitor_a": self.monitor_a,
            "monitor_b": self.monitor_b,
            "registry_id": self.registry_id,
            "divergent": self.divergent,
        }
