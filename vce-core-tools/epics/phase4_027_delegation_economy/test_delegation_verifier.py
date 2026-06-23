from epics.phase4_027_delegation_economy.delegation_state import (
    DelegationState,
)
from epics.phase4_027_delegation_economy.delegation_verifier import (
    verify_delegation_state,
)


def test_verification_succeeds_when_capacity_is_available():
    state = DelegationState(
        delegator_id="institution.alpha",
        active_delegations=2,
        total_delegated_capacity=40,
    )

    result = verify_delegation_state(
        state=state,
        available_capital=100,
    )

    assert result["verified"] is True


def test_verification_fails_when_capacity_exceeded():
    state = DelegationState(
        delegator_id="institution.alpha",
        active_delegations=3,
        total_delegated_capacity=120,
    )

    result = verify_delegation_state(
        state=state,
        available_capital=100,
    )

    assert result["verified"] is False


def test_reports_remaining_capacity():
    state = DelegationState(
        delegator_id="institution.alpha",
        active_delegations=1,
        total_delegated_capacity=25,
    )

    result = verify_delegation_state(
        state=state,
        available_capital=100,
    )

    assert result["remaining_capacity"] == 75
