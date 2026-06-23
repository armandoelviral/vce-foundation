from dataclasses import dataclass

from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)


@dataclass(frozen=True)
class MarketState:
    settlement_count: int
    total_settled_value: int
    total_quantity: int

    @classmethod
    def from_settlements(
        cls,
        settlements: list[MarketSettlementRecord],
    ):
        return cls(
            settlement_count=len(settlements),
            total_settled_value=sum(
                settlement.settled_value
                for settlement in settlements
            ),
            total_quantity=sum(
                settlement.quantity
                for settlement in settlements
            ),
        )
