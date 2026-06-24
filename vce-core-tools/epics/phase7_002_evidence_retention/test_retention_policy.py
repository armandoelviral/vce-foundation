from epics.phase7_002_evidence_retention.retention_policy import (
    retention_active,
)


def test_retention_policy_active():
    assert retention_active(25) is True


def test_retention_policy_inactive():
    assert retention_active(0) is False
