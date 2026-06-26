from epics.phase9_005_constitutional_delegation.delegation_state import (
    DelegationState,
)
from epics.phase9_005_constitutional_delegation.delegation_verifier import (
    verify_delegation,
)


def test_verify_delegation():
    state = DelegationState(
        total_delegations=2,
        unique_assignees=2,
    )

    result = verify_delegation(state)

    assert result["verified"] is True


def test_empty_delegation():
    state = DelegationState(
        total_delegations=0,
        unique_assignees=0,
    )

    result = verify_delegation(state)

    assert result["verified"] is False
