from epics.phase4_034_constitutional_liquidity.liquidity_state import (
    LiquidityState,
)


def verify_liquidity_state(state: LiquidityState):
    return {
        "verified": state.remaining_liquidity >= 0,
        "total_liquidity": state.total_liquidity,
        "total_consumed": state.total_consumed,
        "remaining_liquidity": state.remaining_liquidity,
    }
