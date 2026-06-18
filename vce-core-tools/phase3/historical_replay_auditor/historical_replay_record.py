from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HistoricalReplayRecord:

    replay_id: str
    bundle_id: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "replay_id": self.replay_id,
            "bundle_id": self.bundle_id,
        }
