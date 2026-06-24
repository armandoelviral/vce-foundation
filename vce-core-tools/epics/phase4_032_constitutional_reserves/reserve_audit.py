from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


def audit_reserves(
    reserves: list[ReserveRecord],
    consumptions: list[ReserveConsumptionRecord],
):
    return {
        "reserve_count": len(reserves),
        "consumption_count": len(consumptions),
        "total_reserves": sum(
            reserve.reserve_amount
            for reserve in reserves
        ),
        "total_consumed": sum(
            consumption.consumed_amount
            for consumption in consumptions
        ),
    }
