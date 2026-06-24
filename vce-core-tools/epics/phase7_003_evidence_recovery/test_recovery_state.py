from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)
from epics.phase7_003_evidence_recovery.recovery_state import (
    RecoveryState,
)


def test_builds_recovery_state():
    records = [
        RecoveryRecord(
            "recovery.001",
            "evidence.001",
            "backup_restore",
        ),
        RecoveryRecord(
            "recovery.002",
            "evidence.002",
            "replica_restore",
        ),
    ]

    state = RecoveryState.from_records(records)

    assert state.total_records == 2
    assert state.total_recoveries == 2


def test_empty_recovery_state():
    state = RecoveryState.from_records([])

    assert state.total_records == 0
    assert state.total_recoveries == 0
