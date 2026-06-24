from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


def test_liquidity_record_creation():
    record = LiquidityRecord(
        liquidity_id="liq.001",
        source_id="treasury.001",
        liquidity_amount=100,
        purpose="emergency response",
    )

    assert record.liquidity_id == "liq.001"
    assert record.source_id == "treasury.001"
    assert record.liquidity_amount == 100
    assert record.purpose == "emergency response"


def test_rejects_empty_liquidity_id():
    try:
        LiquidityRecord(
            liquidity_id="",
            source_id="treasury.001",
            liquidity_amount=100,
            purpose="test",
        )
        assert False
    except ValueError as exc:
        assert "liquidity_id" in str(exc)


def test_rejects_non_positive_amount():
    try:
        LiquidityRecord(
            liquidity_id="liq.001",
            source_id="treasury.001",
            liquidity_amount=0,
            purpose="test",
        )
        assert False
    except ValueError as exc:
        assert "liquidity_amount" in str(exc)
