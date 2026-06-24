from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)
from epics.phase4_035_constitutional_stability.stability_registry import (
    StabilityRegistry,
)


def test_registry_stores_record():
    registry = StabilityRegistry()

    record = StabilityRecord(
        "stability.001",
        "treasury.001",
        100,
        "continuity",
    )

    registry.add(record)

    assert len(registry.records()) == 1


def test_rejects_duplicate():
    registry = StabilityRegistry()

    record = StabilityRecord(
        "stability.001",
        "treasury.001",
        100,
        "continuity",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = StabilityRegistry()

    record = StabilityRecord(
        "stability.001",
        "treasury.001",
        100,
        "continuity",
    )

    registry.add(record)

    items = registry.records()

    items.clear()

    assert len(registry.records()) == 1
