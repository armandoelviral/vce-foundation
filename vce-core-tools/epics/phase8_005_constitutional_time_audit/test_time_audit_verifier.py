from epics.phase8_005_constitutional_time_audit.time_audit_state import (
    TimeAuditState,
)
from epics.phase8_005_constitutional_time_audit.time_audit_verifier import (
    verify_time_audit,
)


def test_time_audit_verified():
    state = TimeAuditState(
        total_records=2,
        latest_epoch=200,
    )

    result = verify_time_audit(state)

    assert result["verified"] is True


def test_empty_time_audit_not_verified():
    state = TimeAuditState(
        total_records=0,
        latest_epoch=0,
    )

    result = verify_time_audit(state)

    assert result["verified"] is False
