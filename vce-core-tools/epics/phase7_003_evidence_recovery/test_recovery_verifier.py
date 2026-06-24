from epics.phase7_003_evidence_recovery.recovery_state import (
    RecoveryState,
)
from epics.phase7_003_evidence_recovery.recovery_verifier import (
    verify_recovery,
)


def test_recovery_verified():
    state = RecoveryState(
        total_records=2,
        total_recoveries=2,
    )

    result = verify_recovery(state)

    assert result["verified"] is True


def test_empty_recovery_not_verified():
    state = RecoveryState(
        total_records=0,
        total_recoveries=0,
    )

    result = verify_recovery(state)

    assert result["verified"] is False
