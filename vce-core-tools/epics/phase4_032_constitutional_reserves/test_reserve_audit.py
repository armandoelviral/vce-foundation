from epics.phase4_032_constitutional_reserves.reserve_audit import (
    audit_reserves,
)
from epics.phase4_032_constitutional_reserves.reserve_consumption import (
    ReserveConsumptionRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


def test_reserve_audit():
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

    audit = audit_reserves(
        reserves=reserves,
        consumptions=consumptions,
    )

    assert audit["reserve_count"] == 1
    assert audit["consumption_count"] == 1
    assert audit["total_reserves"] == 100
    assert audit["total_consumed"] == 40


def test_empty_audit():
    audit = audit_reserves(
        reserves=[],
        consumptions=[],
    )

    assert audit["reserve_count"] == 0
    assert audit["consumption_count"] == 0
