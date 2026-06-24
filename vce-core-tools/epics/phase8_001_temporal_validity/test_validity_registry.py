from epics.phase8_001_temporal_validity.validity_record import (
    ValidityRecord,
)
from epics.phase8_001_temporal_validity.validity_registry import (
    ValidityRegistry,
)


def test_registry_adds_record():
    registry = ValidityRegistry()

    record = ValidityRecord(
        "validity.001",
        "evidence.001",
        365,
    )

    registry.add(record)

    assert registry.records() == [record]
