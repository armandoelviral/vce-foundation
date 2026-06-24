from dataclasses import dataclass

from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


@dataclass(frozen=True)
class ReserveState:
    total_reserves: int
    total_consumed: int
    remaining_reserves: int

    @classmethod
    def from_records(
        cls,
        reserves: list[ReserveRecord],
        consumptions: list[ReserveConsumptionRecord],
    ):
        total_reserves = sum(
            reserve.reserve_amount
            for reserve in reserves
        )

        total_consumed = sum(
            consumption.consumed_amount
            for consumption in consumptions
        )

        return cls(
            total_reserves=total_reserves,
            total_consumed=total_consumed,
            remaining_reserves=(
                total_reserves - total_consumed
            ),
        )
