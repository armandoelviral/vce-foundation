from epics.phase7_003_evidence_recovery.recovery_record import (
    RecoveryRecord,
)


def test_recovery_record_creation():
    record = RecoveryRecord(
        recovery_id="recovery.001",
        evidence_id="evidence.001",
        recovery_type="backup_restore",
    )

    assert record.recovery_id == "recovery.001"


def test_requires_recovery_id():
    try:
        RecoveryRecord(
            "",
            "evidence.001",
            "backup_restore",
        )
        assert False
    except ValueError as exc:
        assert "recovery_id" in str(exc)
