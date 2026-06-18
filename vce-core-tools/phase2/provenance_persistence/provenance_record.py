from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProvenanceRecord:

    subject_id: str
    origin_id: str
    provenance_hash: str

    def to_dict(self) -> Dict[str, str]:

        return {
            "subject_id": self.subject_id,
            "origin_id": self.origin_id,
            "provenance_hash": self.provenance_hash,
        }
