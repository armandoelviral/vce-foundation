from epics.phase4_033_constitutional_treasury.treasury_allocation import (
    calculate_allocated_reserves,
)
from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)


def test_calculates_allocated_reserves():
    records = [
        TreasuryRecord(
            treasury_id="treasury.001",
            authority_id="treasury.council",
            allocation_amount=100,
            reserve_reference="reserve.001",
        ),
        TreasuryRecord(
            treasury_id="treasury.002",
            authority_id="treasury.council",
            allocation_amount=50,
            reserve_reference="reserve.002",
        ),
    ]

    assert calculate_allocated_reserves(records) == 150


def test_empty_allocation():
    assert calculate_allocated_reserves([]) == 0


def test_single_allocation():
    records = [
        TreasuryRecord(
            treasury_id="treasury.001",
            authority_id="treasury.council",
            allocation_amount=75,
            reserve_reference="reserve.001",
        )
    ]

    assert calculate_allocated_reserves(records) == 75
