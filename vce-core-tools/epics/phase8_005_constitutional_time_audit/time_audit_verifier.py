from epics.phase8_005_constitutional_time_audit.time_audit_state import (
    TimeAuditState,
)


def verify_time_audit(
    state: TimeAuditState,
):
    return {
        "verified": state.latest_epoch > 0,
        "latest_epoch": state.latest_epoch,
        "total_records": state.total_records,
    }
