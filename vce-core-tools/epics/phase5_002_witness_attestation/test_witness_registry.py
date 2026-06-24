from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)
from epics.phase5_002_witness_attestation.witness_registry import (
    WitnessRegistry,
)


def test_registry_stores_witness():
    registry = WitnessRegistry()

    record = WitnessRecord(
        "witness.001",
        "obs.001",
        "human",
    )

    registry.add(record)

    assert len(registry.records()) == 1


def test_rejects_duplicate_witness():
    registry = WitnessRegistry()

    record = WitnessRecord(
        "witness.001",
        "obs.001",
        "human",
    )

    registry.add(record)

    try:
        registry.add(record)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = WitnessRegistry()

    record = WitnessRecord(
        "witness.001",
        "obs.001",
        "human",
    )

    registry.add(record)

    items = registry.records()

    items.clear()

    assert len(registry.records()) == 1
