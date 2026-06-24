from epics.phase4_034_constitutional_liquidity.liquidity_consumption import (
    LiquidityConsumptionRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_record import (
    LiquidityRecord,
)
from epics.phase4_034_constitutional_liquidity.liquidity_registry import (
    LiquidityRegistry,
)
from epics.phase4_034_constitutional_liquidity.liquidity_state import (
    LiquidityState,
)
from epics.phase4_034_constitutional_liquidity.liquidity_verifier import (
    verify_liquidity_state,
)


def test_end_to_end_liquidity_flow():
    registry = LiquidityRegistry()

    registry.add(
        LiquidityRecord(
            liquidity_id="liq.001",
            source_id="treasury.001",
            liquidity_amount=100,
            purpose="immediate obligation support",
        )
    )

    consumption = LiquidityConsumptionRecord(
        consumption_id="consumption.001",
        liquidity_id="liq.001",
        consumed_amount=40,
        reason="urgent constitutional obligation settlement",
    )

    state = LiquidityState.from_records(
        liquidity_records=registry.records(),
        consumptions=[consumption],
    )

    assert state.total_liquidity == 100
    assert state.total_consumed == 40
    assert state.remaining_liquidity == 60

    verification = verify_liquidity_state(state)

    assert verification["verified"] is True
