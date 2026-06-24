from dataclasses import dataclass


@dataclass(frozen=True)
class StabilityRecord:
    stability_id: str
    source_id: str
    stability_amount: int
    rationale: str

    def __post_init__(self):
        if not self.stability_id:
            raise ValueError("stability_id is required")

        if not self.source_id:
            raise ValueError("source_id is required")

        if self.stability_amount <= 0:
            raise ValueError(
                "stability_amount must be positive"
            )

        if not self.rationale:
            raise ValueError("rationale is required")
