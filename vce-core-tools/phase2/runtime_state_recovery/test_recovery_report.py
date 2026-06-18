from phase2.runtime_state_recovery.recovery_report import (
    RecoveryReport,
)


def test_report_contains_recovery_id():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    assert report.recovery_id == "recovery-001"


def test_report_contains_recovery_status():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    assert report.recovered is True


def test_report_contains_hash_verification_status():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=False,
    )

    assert report.state_hash_valid is False


def test_report_serializes():

    report = RecoveryReport(
        recovery_id="recovery-001",
        recovered=True,
        state_hash_valid=True,
    )

    assert report.to_dict() == {
        "recovery_id": "recovery-001",
        "recovered": True,
        "state_hash_valid": True,
    }
