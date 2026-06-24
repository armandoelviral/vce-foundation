from epics.phase7_004_evidence_durability.durability_record import (
    DurabilityRecord,
)
from epics.phase7_004_evidence_durability.durability_registry import (
    DurabilityRegistry,
)


def test_registry_adds_record():
    registry = DurabilityRegistry()

    record = DurabilityRecord(
        "dur.001",
        "evidence.001",
        50,
    )

    registry.add(record)

    assert registry.records() == [record]
