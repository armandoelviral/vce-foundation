from epics.phase4_027_delegation_economy.delegation_revocation import (
    DelegationRevocationRecord,
)


def test_revocation_record_creation():
    record = DelegationRevocationRecord(
        revocation_id="revocation.001",
        delegation_id="delegation.001",
        reason="constitutional violation",
    )

    assert record.revocation_id == "revocation.001"
    assert record.delegation_id == "delegation.001"
    assert record.reason == "constitutional violation"


def test_rejects_empty_revocation_id():
    try:
        DelegationRevocationRecord(
            revocation_id="",
            delegation_id="delegation.001",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "revocation_id" in str(exc)


def test_rejects_empty_delegation_id():
    try:
        DelegationRevocationRecord(
            revocation_id="revocation.001",
            delegation_id="",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "delegation_id" in str(exc)


def test_rejects_empty_reason():
    try:
        DelegationRevocationRecord(
            revocation_id="revocation.001",
            delegation_id="delegation.001",
            reason="",
        )
        assert False
    except ValueError as exc:
        assert "reason" in str(exc)
