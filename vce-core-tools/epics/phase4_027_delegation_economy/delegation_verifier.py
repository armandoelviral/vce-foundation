from epics.phase4_027_delegation_economy.delegation_state import (
    DelegationState,
)


def verify_delegation_state(
    state: DelegationState,
    available_capital: int,
) -> dict:

    remaining_capacity = (
        available_capital
        - state.total_delegated_capacity
    )

    return {
        "delegator_id": state.delegator_id,
        "verified": remaining_capacity >= 0,
        "remaining_capacity": remaining_capacity,
        "available_capital": available_capital,
        "delegated_capacity": state.total_delegated_capacity,
    }
