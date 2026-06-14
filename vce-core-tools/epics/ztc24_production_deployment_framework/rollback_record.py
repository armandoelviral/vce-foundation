from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RollbackRecord:

    failed_release_id: str
    restored_release_id: str
    reason: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "failed_release_id": self.failed_release_id,
            "restored_release_id": self.restored_release_id,
            "reason": self.reason,
        }
