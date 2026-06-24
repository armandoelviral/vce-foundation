from epics.phase8_005_constitutional_time_audit.time_audit_record import (
    TimeAuditRecord,
)
from epics.phase8_005_constitutional_time_audit.time_audit_state import (
    TimeAuditState,
)


def test_builds_time_audit_state():
    records = [
        TimeAuditRecord(
            "audit.001",
            "snapshot.001",
            100,
        ),
        TimeAuditRecord(
            "audit.002",
            "snapshot.002",
            200,
        ),
    ]

    state = TimeAuditState.from_records(records)

    assert state.total_records == 2
    assert state.latest_epoch == 200


def test_empty_time_audit_state():
    state = TimeAuditState.from_records([])

    assert state.total_records == 0
    assert state.latest_epoch == 0
