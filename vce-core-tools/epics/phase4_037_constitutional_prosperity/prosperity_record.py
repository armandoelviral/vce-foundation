from dataclasses import dataclass


@dataclass(frozen=True)
class ProsperityRecord:
    prosperity_id: str
    source_id: str
    prosperity_amount: int
    rationale: str

    def __post_init__(self):
        if not self.prosperity_id:
            raise ValueError("prosperity_id is required")

        if not self.source_id:
            raise ValueError("source_id is required")

        if self.prosperity_amount <= 0:
            raise ValueError("prosperity_amount must be positive")

        if not self.rationale:
            raise ValueError("rationale is required")
