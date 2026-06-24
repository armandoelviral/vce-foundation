from dataclasses import dataclass

from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


@dataclass(frozen=True)
class LiquidityState:
    total_liquidity: int
    total_consumed: int
    remaining_liquidity: int

    @classmethod
    def from_records(
        cls,
        liquidity_records: list[LiquidityRecord],
        consumptions: list[LiquidityConsumptionRecord],
    ):
        total_liquidity = sum(
            record.liquidity_amount for record in liquidity_records
        )
        total_consumed = sum(
            consumption.consumed_amount for consumption in consumptions
        )

        return cls(
            total_liquidity=total_liquidity,
            total_consumed=total_consumed,
            remaining_liquidity=total_liquidity - total_consumed,
        )
