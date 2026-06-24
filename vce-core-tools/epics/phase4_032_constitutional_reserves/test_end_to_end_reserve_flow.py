from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_registry import (
    ReserveRegistry,
)
from epics.phase4_032_constitutional_reserves.reserve_state import (
    ReserveState,
)
from epics.phase4_032_constitutional_reserves.reserve_verifier import (
    verify_reserve_state,
)


def test_end_to_end_reserve_flow():
    registry = ReserveRegistry()

    registry.add(
        ReserveRecord(
            reserve_id="reserve.001",
            institution_id="institution.alpha",
            reserve_amount=100,
            source_reference="capital.001",
        )
    )

    consumption = ReserveConsumptionRecord(
        consumption_id="consumption.001",
        reserve_id="reserve.001",
        consumed_amount=40,
        reason="insurance payout",
    )

    state = ReserveState.from_records(
        reserves=registry.records(),
        consumptions=[consumption],
    )

    assert state.total_reserves == 100
    assert state.total_consumed == 40
    assert state.remaining_reserves == 60

    verification = verify_reserve_state(state)

    assert verification["verified"] is True
