from epics.phase4_028_constitutional_markets.market_settlement import (
    MarketSettlementRecord,
)


def audit_market_settlements(
    settlements: list[MarketSettlementRecord],
) -> dict:
    return {
        "settlement_count": len(settlements),
        "total_settled_value": sum(
            settlement.settled_value
            for settlement in settlements
        ),
        "total_quantity": sum(
            settlement.quantity
            for settlement in settlements
        ),
        "settlements": list(settlements),
    }
