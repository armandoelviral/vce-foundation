from epics.phase4_036_constitutional_sustainability.sustainability_record import SustainabilityRecord
from epics.phase4_036_constitutional_sustainability.sustainability_registry import SustainabilityRegistry


def test_registry_stores_record():
    registry = SustainabilityRegistry()

    registry.add(
        SustainabilityRecord(
            "sus.001",
            "stability.001",
            100,
            "continuity",
        )
    )

    assert len(registry.records()) == 1


def test_rejects_duplicate():
    registry = SustainabilityRegistry()

    record = SustainabilityRecord(
        "sus.001",
        "stability.001",
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
    registry = SustainabilityRegistry()

    registry.add(
        SustainabilityRecord(
            "sus.001",
            "stability.001",
            100,
            "continuity",
        )
    )

    items = registry.records()

    items.clear()

    assert len(registry.records()) == 1
