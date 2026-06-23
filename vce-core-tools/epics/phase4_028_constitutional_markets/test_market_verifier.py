from epics.phase4_028_constitutional_markets.market_state import (
    MarketState,
)
from epics.phase4_028_constitutional_markets.market_verifier import (
    verify_market_state,
)


def test_market_verification_success():
    state = MarketState(
        settlement_count=2,
        total_settled_value=160,
        total_quantity=75,
    )

    result = verify_market_state(state)

    assert result["verified"] is True


def test_market_rejects_negative_value():
    state = MarketState(
        settlement_count=2,
        total_settled_value=-1,
        total_quantity=75,
    )

    result = verify_market_state(state)

    assert result["verified"] is False


def test_market_rejects_negative_quantity():
    state = MarketState(
        settlement_count=2,
        total_settled_value=160,
        total_quantity=-1,
    )

    result = verify_market_state(state)

    assert result["verified"] is False


def test_market_rejects_negative_settlement_count():
    state = MarketState(
        settlement_count=-1,
        total_settled_value=160,
        total_quantity=75,
    )

    result = verify_market_state(state)

    assert result["verified"] is False
