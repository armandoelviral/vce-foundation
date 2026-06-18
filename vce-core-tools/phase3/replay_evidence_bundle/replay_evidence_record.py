from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReplayEvidenceRecord:

    evidence_id: str
    evidence_type: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type,
        }
