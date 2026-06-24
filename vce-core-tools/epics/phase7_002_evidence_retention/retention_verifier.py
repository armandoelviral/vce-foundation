from epics.phase7_002_evidence_retention.retention_state import (
    RetentionState,
)


def verify_retention(
    state: RetentionState,
):
    return {
        "verified": state.total_years > 0,
        "total_years": state.total_years,
        "total_records": state.total_records,
    }
