from dataclasses import dataclass


@dataclass(frozen=True)
class SustainabilityRecord:
    sustainability_id: str
    source_id: str
    sustainability_amount: int
    rationale: str

    def __post_init__(self):
        if not self.sustainability_id:
            raise ValueError("sustainability_id is required")

        if not self.source_id:
            raise ValueError("source_id is required")

        if self.sustainability_amount <= 0:
            raise ValueError(
                "sustainability_amount must be positive"
            )

        if not self.rationale:
            raise ValueError("rationale is required")
