from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayAuditDecision:

    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "status": self.status
        }
