from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayRevocationRecord:

    revocation_id: str
    certificate_id: str
    reason: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "revocation_id": self.revocation_id,
            "certificate_id": self.certificate_id,
            "reason": self.reason,
        }
