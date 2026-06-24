from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_state import (
    LiquidityState,
)


def test_builds_liquidity_state():
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

    state = LiquidityState.from_records(
        liquidity_records=liquidity_records,
        consumptions=consumptions,
    )

    assert state.total_liquidity == 100
    assert state.total_consumed == 40
    assert state.remaining_liquidity == 60


def test_empty_liquidity_state():
    state = LiquidityState.from_records([], [])

    assert state.total_liquidity == 0
    assert state.total_consumed == 0
    assert state.remaining_liquidity == 0
