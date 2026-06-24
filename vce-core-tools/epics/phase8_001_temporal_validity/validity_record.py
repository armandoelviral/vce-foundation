from dataclasses import dataclass


@dataclass(frozen=True)
class ValidityRecord:
    validity_id: str
    evidence_id: str
    valid_days: int

    def __post_init__(self):
        if not self.validity_id:
            raise ValueError("validity_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")
