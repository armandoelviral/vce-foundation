from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AttestationEvidence:

    witness_id: str
    provider: str
    evidence_hash: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "witness_id": self.witness_id,
            "provider": self.provider,
            "evidence_hash": self.evidence_hash,
        }
