from dataclasses import dataclass


@dataclass(frozen=True)
class RetentionRecord:
    retention_id: str
    evidence_id: str
    retention_years: int

    def __post_init__(self):
        if not self.retention_id:
            raise ValueError("retention_id is required")

        if not self.evidence_id:
            raise ValueError("evidence_id is required")
