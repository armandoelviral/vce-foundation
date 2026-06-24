from epics.phase4_034_constitutional_liquidity.liquidity_audit import (
    audit_liquidity,
)
from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


def test_liquidity_audit():
    liquidity_records = [
        LiquidityRecord("liq.001", "treasury.001", 100, "response")
    ]
    consumptions = [
        LiquidityConsumptionRecord(
            "consumption.001",
            "liq.001",
            40,
            "obligation settlement",
        )
    ]

    audit = audit_liquidity(liquidity_records, consumptions)

    assert audit["liquidity_count"] == 1
    assert audit["consumption_count"] == 1
    assert audit["total_liquidity"] == 100
    assert audit["total_consumed"] == 40


def test_empty_liquidity_audit():
    audit = audit_liquidity([], [])

    assert audit["liquidity_count"] == 0
    assert audit["consumption_count"] == 0
    assert audit["total_liquidity"] == 0
    assert audit["total_consumed"] == 0
