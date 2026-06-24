from epics.phase7_003_evidence_recovery.recovery_state import (
    RecoveryState,
)


def verify_recovery(
    state: RecoveryState,
):
    return {
        "verified": state.total_recoveries > 0,
        "total_recoveries": state.total_recoveries,
        "total_records": state.total_records,
    }
