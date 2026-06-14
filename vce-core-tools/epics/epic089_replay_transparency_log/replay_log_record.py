from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayLogRecord:
    sequence: int
    previous_hash: str
    current_hash: str
    replay_id: str

    def to_dict(self) -> Dict:
        return {
            "sequence": self.sequence,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
            "replay_id": self.replay_id,
        }
