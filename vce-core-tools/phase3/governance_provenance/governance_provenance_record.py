from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class GovernanceProvenanceRecord:

    provenance_id: str
    current_snapshot: str
    previous_snapshot: str

    def to_dict(
        self,
    ) -> Dict[str, str]:

        return {
            "provenance_id":
                self.provenance_id,
            "current_snapshot":
                self.current_snapshot,
            "previous_snapshot":
                self.previous_snapshot,
        }
