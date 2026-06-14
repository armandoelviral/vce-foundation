from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class WitnessProviderMetadata:
    witness_id: str
    cloud_provider: str
    region: str
    kms_provider: str
    confidential_compute_profile: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "witness_id": self.witness_id,
            "cloud_provider": self.cloud_provider,
            "region": self.region,
            "kms_provider": self.kms_provider,
            "confidential_compute_profile": self.confidential_compute_profile,
        }
