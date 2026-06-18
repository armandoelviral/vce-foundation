from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AttestationRecord:

    attestation_id: str
    subject: str
    evidence_hash: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "attestation_id": self.attestation_id,
            "subject": self.subject,
            "evidence_hash": self.evidence_hash,
        }
