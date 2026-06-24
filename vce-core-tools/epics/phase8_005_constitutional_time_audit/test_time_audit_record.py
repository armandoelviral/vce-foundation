from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)


def test_time_audit_record_creation():
    record = TimeAuditRecord(
        audit_id="audit.001",
        snapshot_id="snapshot.001",
        epoch=100,
    )

    assert record.audit_id == "audit.001"


def test_requires_audit_id():
    try:
        TimeAuditRecord(
            "",
            "snapshot.001",
            100,
        )
        assert False
    except ValueError as exc:
        assert "audit_id" in str(exc)
