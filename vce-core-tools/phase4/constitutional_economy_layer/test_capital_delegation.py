from phase4.constitutional_economy_layer.capital_delegation import (
    CapitalDelegation,
)


def test_contains_delegator():

    delegation = CapitalDelegation(
        delegator_id="identity-001",
        delegate_id="identity-002",
        amount=25,
    )

    assert delegation.delegator_id == "identity-001"


def test_contains_delegate():

    delegation = CapitalDelegation(
        delegator_id="identity-001",
        delegate_id="identity-002",
        amount=25,
    )

    assert delegation.delegate_id == "identity-002"


def test_contains_amount():

    delegation = CapitalDelegation(
        delegator_id="identity-001",
        delegate_id="identity-002",
        amount=25,
    )

    assert delegation.amount == 25


def test_serializes():

    delegation = CapitalDelegation(
        delegator_id="identity-001",
        delegate_id="identity-002",
        amount=25,
    )

    assert delegation.to_dict() == {
        "delegator_id": "identity-001",
        "delegate_id": "identity-002",
        "amount": 25,
    }
