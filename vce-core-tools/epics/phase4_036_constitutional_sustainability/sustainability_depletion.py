from dataclasses import dataclass


@dataclass(frozen=True)
class SustainabilityDepletionRecord:
    depletion_id: str
    sustainability_id: str
    depletion_amount: int
    reason: str

    def __post_init__(self):
        if not self.depletion_id:
            raise ValueError("depletion_id is required")

        if not self.sustainability_id:
            raise ValueError("sustainability_id is required")

        if self.depletion_amount <= 0:
            raise ValueError(
                "depletion_amount must be positive"
            )

        if not self.reason:
            raise ValueError("reason is required")
