from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


def audit_liquidity(
    liquidity_records: list[LiquidityRecord],
    consumptions: list[LiquidityConsumptionRecord],
):
    return {
        "liquidity_count": len(liquidity_records),
        "consumption_count": len(consumptions),
        "total_liquidity": sum(
            record.liquidity_amount for record in liquidity_records
        ),
        "total_consumed": sum(
            consumption.consumed_amount for consumption in consumptions
        ),
    }
