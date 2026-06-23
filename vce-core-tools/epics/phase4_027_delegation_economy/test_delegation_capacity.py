from epics.phase4_027_delegation_economy.delegation_capacity import (
    calculate_remaining_delegation_capacity,
)
from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)
from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)


def test_remaining_capacity_without_delegations():
    registry = DelegationRegistry()

    remaining = calculate_remaining_delegation_capacity(
        registry=registry,
        delegator_id="institution.alpha",
        available_capital=100,
    )

    assert remaining == 100


def test_remaining_capacity_after_delegations():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="constitutional sponsorship",
        )
    )

    registry.add(
        DelegationRecord(
            delegation_id="delegation.002",
            delegator_id="institution.alpha",
            delegate_id="citizen.gamma",
            delegated_capacity=30,
            reason="institutional backing",
        )
    )

    remaining = calculate_remaining_delegation_capacity(
        registry=registry,
        delegator_id="institution.alpha",
        available_capital=100,
    )

    assert remaining == 45


def test_capacity_is_isolated_by_delegator():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="alpha delegation",
        )
    )

    registry.add(
        DelegationRecord(
            delegation_id="delegation.002",
            delegator_id="institution.beta",
            delegate_id="citizen.gamma",
            delegated_capacity=80,
            reason="beta delegation",
        )
    )

    remaining = calculate_remaining_delegation_capacity(
        registry=registry,
        delegator_id="institution.alpha",
        available_capital=100,
    )

    assert remaining == 75


def test_rejects_negative_available_capital():
    registry = DelegationRegistry()

    try:
        calculate_remaining_delegation_capacity(
            registry=registry,
            delegator_id="institution.alpha",
            available_capital=-1,
        )
        assert False
    except ValueError as exc:
        assert "available_capital" in str(exc)
