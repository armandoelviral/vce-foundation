from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayProvenanceCertificate:
    replay_id: str
    request_hash: str
    result_hash: str
    environment_hash: str
    comparator_hash: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "replay_id": self.replay_id,
            "request_hash": self.request_hash,
            "result_hash": self.result_hash,
            "environment_hash": self.environment_hash,
            "comparator_hash": self.comparator_hash,
        }

