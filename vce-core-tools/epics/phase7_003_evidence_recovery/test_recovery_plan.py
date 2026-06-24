from epics.phase7_003_evidence_recovery.recovery_plan import (
    recovery_possible,
)


def test_recovery_possible():
    assert recovery_possible("backup_restore") is True


def test_unknown_recovery_not_possible():
    assert recovery_possible("") is False
