from epics.phase7_002_evidence_retention.retention_record import (
    RetentionRecord,
)
from epics.phase7_002_evidence_retention.retention_registry import (
    RetentionRegistry,
)


def test_registry_adds_record():
    registry = RetentionRegistry()

    record = RetentionRecord(
        "ret.001",
        "evidence.001",
        25,
    )

    registry.add(record)

    assert registry.records() == [record]
