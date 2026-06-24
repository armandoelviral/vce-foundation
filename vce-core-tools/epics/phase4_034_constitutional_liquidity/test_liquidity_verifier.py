from epics.phase4_034_constitutional_liquidity.liquidity_state import (
    LiquidityState,
)
from epics.phase4_034_constitutional_liquidity.liquidity_verifier import (
    verify_liquidity_state,
)


def test_liquidity_verification_succeeds():
    state = LiquidityState(
        total_liquidity=100,
        total_consumed=40,
        remaining_liquidity=60,
    )

    result = verify_liquidity_state(state)

    assert result["verified"] is True


def test_liquidity_verification_fails():
    state = LiquidityState(
        total_liquidity=100,
        total_consumed=120,
        remaining_liquidity=-20,
    )

    result = verify_liquidity_state(state)

    assert result["verified"] is False


def test_reports_remaining_liquidity():
    state = LiquidityState(
        total_liquidity=100,
        total_consumed=25,
        remaining_liquidity=75,
    )

    result = verify_liquidity_state(state)

    assert result["remaining_liquidity"] == 75
