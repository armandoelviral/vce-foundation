from epics.phase4_032_constitutional_reserves.reserve_capacity import (
    calculate_total_reserves,
)
from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)


def test_calculates_total_reserves():
    records = [
        ReserveRecord(
            reserve_id="reserve.001",
            institution_id="institution.alpha",
            reserve_amount=100,
            source_reference="capital.001",
        ),
        ReserveRecord(
            reserve_id="reserve.002",
            institution_id="institution.alpha",
            reserve_amount=50,
            source_reference="capital.002",
        ),
    ]

    assert calculate_total_reserves(records) == 150


def test_empty_reserves():
    assert calculate_total_reserves([]) == 0


def test_single_reserve():
    records = [
        ReserveRecord(
            reserve_id="reserve.001",
            institution_id="institution.alpha",
            reserve_amount=75,
            source_reference="capital.001",
        )
    ]

    assert calculate_total_reserves(records) == 75
