from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)
from epics.phase7_003_evidence_recovery.recovery_registry import (
    RecoveryRegistry,
)
from epics.phase7_003_evidence_recovery.recovery_state import (
    RecoveryState,
)
from epics.phase7_003_evidence_recovery.recovery_verifier import (
    verify_recovery,
)


def test_end_to_end_recovery_flow():
    registry = RecoveryRegistry()

    registry.add(
        RecoveryRecord(
            "recovery.001",
            "evidence.001",
            "backup_restore",
        )
    )

    registry.add(
        RecoveryRecord(
            "recovery.002",
            "evidence.002",
            "replica_restore",
        )
    )

    state = RecoveryState.from_records(
        registry.records()
    )

    verification = verify_recovery(state)

    assert verification["verified"] is True
    assert verification["total_recoveries"] == 2
