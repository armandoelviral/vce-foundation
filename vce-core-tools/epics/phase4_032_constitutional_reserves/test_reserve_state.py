from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_state import (
    ReserveState,
)


def test_builds_reserve_state():
    reserves = [
        ReserveRecord(
            reserve_id="reserve.001",
            institution_id="institution.alpha",
            reserve_amount=100,
            source_reference="capital.001",
        )
    ]

    consumptions = [
        ReserveConsumptionRecord(
            consumption_id="consumption.001",
            reserve_id="reserve.001",
            consumed_amount=40,
            reason="insurance payout",
        )
    ]

    state = ReserveState.from_records(
        reserves=reserves,
        consumptions=consumptions,
    )

    assert state.total_reserves == 100
    assert state.total_consumed == 40
    assert state.remaining_reserves == 60


def test_empty_state():
    state = ReserveState.from_records(
        reserves=[],
        consumptions=[],
    )

    assert state.remaining_reserves == 0
