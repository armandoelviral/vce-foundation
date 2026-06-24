from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)
from epics.phase8_005_constitutional_time_audit.time_audit_registry import (
    TimeAuditRegistry,
)
from epics.phase8_005_constitutional_time_audit.time_audit_report import (
    generate_audit_report,
)
from epics.phase8_005_constitutional_time_audit.time_audit_state import (
    TimeAuditState,
)
from epics.phase8_005_constitutional_time_audit.time_audit_verifier import (
    verify_time_audit,
)


def test_end_to_end_time_audit_flow():
    registry = TimeAuditRegistry()

    registry.add(
        TimeAuditRecord(
            "audit.001",
            "snapshot.001",
            100,
        )
    )

    registry.add(
        TimeAuditRecord(
            "audit.002",
            "snapshot.002",
            200,
        )
    )

    state = TimeAuditState.from_records(
        registry.records()
    )

    verification = verify_time_audit(state)

    report = generate_audit_report(
        snapshot_id="snapshot.002",
        epoch=200,
    )

    assert verification["verified"] is True
    assert verification["latest_epoch"] == 200
    assert report["auditable"] is True
