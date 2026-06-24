from epics.phase5_001_verifiable_observation.observation_record import (
    ObservationRecord,
)
from epics.phase5_001_verifiable_observation.observation_registry import (
    ObservationRegistry,
)


def test_registry_stores_observation():
    registry = ObservationRegistry()

    record = ObservationRecord(
        "obs.001",
        "observer.001",
        "physical",
        "object_detected",
    )

    registry.add(record)

    assert len(registry.records()) == 1


def test_rejects_duplicate_observation():
    registry = ObservationRegistry()

    record = ObservationRecord(
        "obs.001",
        "observer.001",
        "physical",
        "object_detected",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = ObservationRegistry()

    record = ObservationRecord(
        "obs.001",
        "observer.001",
        "physical",
        "object_detected",
    )

    registry.add(record)

    items = registry.records()

    items.clear()

    assert len(registry.records()) == 1
