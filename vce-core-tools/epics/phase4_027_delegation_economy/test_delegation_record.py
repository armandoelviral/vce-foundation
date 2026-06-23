from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)


def test_delegation_record_creation():
    record = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="constitutional sponsorship",
    )

    assert record.delegation_id == "delegation.001"
    assert record.delegator_id == "institution.alpha"
    assert record.delegate_id == "citizen.beta"
    assert record.delegated_capacity == 25
    assert record.reason == "constitutional sponsorship"


def test_rejects_empty_delegation_id():
    try:
        DelegationRecord(
            delegation_id="",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "delegation_id" in str(exc)


def test_rejects_empty_delegator():
    try:
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "delegator_id" in str(exc)


def test_rejects_non_positive_capacity():
    try:
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "delegated_capacity" in str(exc)
