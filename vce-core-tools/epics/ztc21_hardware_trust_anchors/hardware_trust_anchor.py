from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HardwareTrustAnchor:

    provider: str
    anchor_type: str
    measurement_hash: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "provider": self.provider,
            "anchor_type": self.anchor_type,
            "measurement_hash": self.measurement_hash,
        }
