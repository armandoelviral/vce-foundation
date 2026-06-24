from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityConsumptionRecord:
    consumption_id: str
    liquidity_id: str
    consumed_amount: int
    reason: str

    def __post_init__(self):
        if not self.consumption_id:
            raise ValueError("consumption_id is required")

        if not self.liquidity_id:
            raise ValueError("liquidity_id is required")

        if self.consumed_amount <= 0:
            raise ValueError("consumed_amount must be positive")

        if not self.reason:
            raise ValueError("reason is required")
