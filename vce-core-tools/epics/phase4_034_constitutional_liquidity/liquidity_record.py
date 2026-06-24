from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidityRecord:
    liquidity_id: str
    source_id: str
    liquidity_amount: int
    purpose: str

    def __post_init__(self):
        if not self.liquidity_id:
            raise ValueError("liquidity_id is required")
        if not self.source_id:
            raise ValueError("source_id is required")
        if self.liquidity_amount <= 0:
            raise ValueError("liquidity_amount must be positive")
        if not self.purpose:
            raise ValueError("purpose is required")
