from epics.phase4_034_constitutional_liquidity.liquidity_accrual import (
    calculate_total_liquidity,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)


def test_calculates_total_liquidity():
    records = [
        LiquidityRecord("liq.001", "treasury.001", 100, "response"),
        LiquidityRecord("liq.002", "treasury.002", 50, "response"),
    ]

    assert calculate_total_liquidity(records) == 150


def test_empty_liquidity():
    assert calculate_total_liquidity([]) == 0


def test_single_liquidity():
    records = [
        LiquidityRecord("liq.001", "treasury.001", 75, "response")
    ]

    assert calculate_total_liquidity(records) == 75
