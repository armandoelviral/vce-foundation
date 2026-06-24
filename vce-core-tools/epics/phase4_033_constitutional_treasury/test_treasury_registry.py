from epics.phase4_033_constitutional_treasury.treasury_record import (
    TreasuryRecord,
)
from epics.phase4_033_constitutional_treasury.treasury_registry import (
    TreasuryRegistry,
)


def test_registry_stores_treasury_record():
    registry = TreasuryRegistry()

    record = TreasuryRecord(
        treasury_id="treasury.001",
        authority_id="treasury.council",
        allocation_amount=100,
        reserve_reference="reserve.001",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_rejects_duplicate_record():
    registry = TreasuryRegistry()

    record = TreasuryRecord(
        treasury_id="treasury.001",
        authority_id="treasury.council",
        allocation_amount=100,
        reserve_reference="reserve.001",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate treasury" in str(exc)


def test_registry_returns_copy():
    registry = TreasuryRegistry()

    record = TreasuryRecord(
        treasury_id="treasury.001",
        authority_id="treasury.council",
        allocation_amount=100,
        reserve_reference="reserve.001",
    )

    registry.add(record)

    records = registry.records()

    records.clear()

    assert len(registry.records()) == 1
