from epics.phase9_005_constitutional_delegation.delegation_state import (
    DelegationState,
)


def verify_delegation(
    state: DelegationState,
):
    return {
        "verified": state.total_delegations > 0,
        "total_delegations": state.total_delegations,
        "unique_assignees": state.unique_assignees,
    }
