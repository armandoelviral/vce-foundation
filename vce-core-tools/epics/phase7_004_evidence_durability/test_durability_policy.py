from epics.phase7_004_evidence_durability.durability_policy import (
    durable_evidence,
)


def test_evidence_is_durable():
    assert durable_evidence(50) is True


def test_non_durable_evidence():
    assert durable_evidence(0) is False
