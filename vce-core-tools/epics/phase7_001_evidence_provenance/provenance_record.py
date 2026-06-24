from dataclasses import dataclass


@dataclass(frozen=True)
class ProvenanceRecord:
    provenance_id: str
    evidence_id: str
    parent_id: str

    def __post_init__(self):
        if not self.provenance_id:
            raise ValueError("provenance_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")
