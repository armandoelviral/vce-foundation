from dataclasses import dataclass


@dataclass(frozen=True)
class ReserveConsumptionRecord:
    consumption_id: str
    reserve_id: str
    consumed_amount: int
    reason: str

    def __post_init__(self):
        if not self.consumption_id:
            raise ValueError("consumption_id is required")

        if not self.reserve_id:
            raise ValueError("reserve_id is required")

        if self.consumed_amount <= 0:
            raise ValueError("consumed_amount must be positive")

        if not self.reason:
            raise ValueError("reason is required")
