from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayCertificateRecord:

    certificate_id: str
    replay_id: str
    status: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "certificate_id": self.certificate_id,
            "replay_id": self.replay_id,
            "status": self.status,
        }
