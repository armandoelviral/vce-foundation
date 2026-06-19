from phase3.governance_recovery.recovery_record import (
    RecoveryRecord,
)

from phase3.governance_recovery.recovery_evaluation import (
    RecoveryEvaluation,
)


def test_manual_remediation_recovers():

    record = RecoveryRecord(
        recovery_id="rec-001",
        incident_id="esc-001",
        recovery_reason="manual_remediation",
    )

    result = RecoveryEvaluation.evaluate(
        record
    )

    assert result is True


def test_automatic_recovery_recovers():

    record = RecoveryRecord(
        recovery_id="rec-002",
        incident_id="esc-002",
        recovery_reason="automatic_recovery",
    )

    result = RecoveryEvaluation.evaluate(
        record
    )

    assert result is True


def test_unverified_fix_does_not_recover():

    record = RecoveryRecord(
        recovery_id="rec-003",
        incident_id="esc-003",
        recovery_reason="unverified_fix",
    )

    result = RecoveryEvaluation.evaluate(
        record
    )

    assert result is False
