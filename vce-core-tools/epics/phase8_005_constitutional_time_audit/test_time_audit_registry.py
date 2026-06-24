from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)
from epics.phase8_005_constitutional_time_audit.time_audit_registry import (
    TimeAuditRegistry,
)


def test_registry_adds_record():
    registry = TimeAuditRegistry()

    record = TimeAuditRecord(
        "audit.001",
        "snapshot.001",
        100,
    )

    registry.add(record)

    assert registry.records() == [record]
