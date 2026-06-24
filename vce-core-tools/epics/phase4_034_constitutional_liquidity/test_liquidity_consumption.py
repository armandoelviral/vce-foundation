from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)


def test_liquidity_consumption_creation():
    record = LiquidityConsumptionRecord(
        consumption_id="consumption.001",
        liquidity_id="liq.001",
        consumed_amount=40,
        reason="immediate obligation settlement",
    )

    assert record.consumption_id == "consumption.001"
    assert record.liquidity_id == "liq.001"
    assert record.consumed_amount == 40
    assert record.reason == "immediate obligation settlement"


def test_rejects_empty_consumption_id():
    try:
        LiquidityConsumptionRecord(
            consumption_id="",
            liquidity_id="liq.001",
            consumed_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "consumption_id" in str(exc)


def test_rejects_non_positive_consumed_amount():
    try:
        LiquidityConsumptionRecord(
            consumption_id="consumption.001",
            liquidity_id="liq.001",
            consumed_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "consumed_amount" in str(exc)
