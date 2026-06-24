from dataclasses import dataclass


@dataclass(frozen=True)
class DurabilityRecord:
    durability_id: str
    evidence_id: str
    durability_years: int

    def __post_init__(self):
        if not self.durability_id:
            raise ValueError("durability_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")
