from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class HybridSignatureEnvelope:
    evidence_hash: str
    classical_signature: str
    pqc_signature: str
    policy_mode: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "evidence_hash": self.evidence_hash,
            "classical_signature": self.classical_signature,
            "pqc_signature": self.pqc_signature,
            "policy_mode": self.policy_mode,
        }
