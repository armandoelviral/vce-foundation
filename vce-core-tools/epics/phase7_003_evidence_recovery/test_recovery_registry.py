from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)
from epics.phase7_003_evidence_recovery.recovery_registry import (
    RecoveryRegistry,
)


def test_registry_adds_record():
    registry = RecoveryRegistry()

    record = RecoveryRecord(
        "recovery.001",
        "evidence.001",
        "backup_restore",
    )

    registry.add(record)

    assert registry.records() == [record]
