from epics.phase4_028_constitutional_markets.market_state import (
    MarketState,
)


def verify_market_state(
    state: MarketState,
) -> dict:

    verified = (
        state.settlement_count >= 0
        and state.total_settled_value >= 0
        and state.total_quantity >= 0
    )

    return {
        "verified": verified,
        "settlement_count": state.settlement_count,
        "total_settled_value": state.total_settled_value,
        "total_quantity": state.total_quantity,
    }
