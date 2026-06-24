from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)
from epics.phase4_037_constitutional_prosperity.prosperity_registry import (
    ProsperityRegistry,
)


def test_registry_stores_prosperity_record():
    registry = ProsperityRegistry()

    record = ProsperityRecord(
        prosperity_id="prosperity.001",
        source_id="sustainability.001",
        prosperity_amount=100,
        rationale="sustainable capacity expansion",
    )

    registry.add(record)

    assert registry.records() == [record]


def test_registry_rejects_duplicate_prosperity():
    registry = ProsperityRegistry()

    record = ProsperityRecord(
        prosperity_id="prosperity.001",
        source_id="sustainability.001",
        prosperity_amount=100,
        rationale="sustainable capacity expansion",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError as exc:
        assert "duplicate prosperity" in str(exc)


def test_registry_returns_copy():
    registry = ProsperityRegistry()

    record = ProsperityRecord(
        prosperity_id="prosperity.001",
        source_id="sustainability.001",
        prosperity_amount=100,
        rationale="sustainable capacity expansion",
    )

    registry.add(record)

    records = registry.records()
    records.clear()

    assert registry.records() == [record]
