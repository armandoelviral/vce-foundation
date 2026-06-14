from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayTransparencyEntry:
    entry_id: str
    replay_id: str
    certificate_hash: str
    certificate_signature: str
    verified: bool

    def to_dict(self) -> Dict:
        return {
            "entry_id": self.entry_id,
            "replay_id": self.replay_id,
            "certificate_hash": self.certificate_hash,
            "certificate_signature": self.certificate_signature,
            "verified": self.verified,
        }
