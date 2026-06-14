from dataclasses import dataclass
from typing import Dict
from typing import Union


@dataclass(frozen=True)
class MonitorVote:

    monitor_id: str
    incident_id: str
    vote: bool

    def to_dict(
        self,
    ) -> Dict[str, Union[str, bool]]:

        return {
            "monitor_id": self.monitor_id,
            "incident_id": self.incident_id,
            "vote": self.vote,
        }
