from epics.phase4_032_constitutional_reserves.reserve_record import (
    ReserveRecord,
)
from epics.phase4_032_constitutional_reserves.reserve_registry import (
    ReserveRegistry,
)


def test_registry_stores_reserve():
    registry = ReserveRegistry()

    reserve = ReserveRecord(
        reserve_id="reserve.001",
        institution_id="institution.alpha",
        reserve_amount=100,
        source_reference="capital.001",
    )

    registry.add(reserve)

    assert registry.records() == [reserve]


def test_registry_rejects_duplicate_reserve():
    registry = ReserveRegistry()

    reserve = ReserveRecord(
        reserve_id="reserve.001",
        institution_id="institution.alpha",
        reserve_amount=100,
        source_reference="capital.001",
    )

    registry.add(reserve)

    try:
        registry.add(reserve)
        assert False
    except ValueError as exc:
        assert "duplicate reserve" in str(exc)


def test_registry_returns_copy():
    registry = ReserveRegistry()

    reserve = ReserveRecord(
        reserve_id="reserve.001",
        institution_id="institution.alpha",
        reserve_amount=100,
        source_reference="capital.001",
    )

    registry.add(reserve)

    records = registry.records()
    records.clear()

    assert len(registry.records()) == 1
