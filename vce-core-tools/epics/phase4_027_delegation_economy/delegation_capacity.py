from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)


def calculate_remaining_delegation_capacity(
    registry: DelegationRegistry,
    delegator_id: str,
    available_capital: int,
) -> int:
    if available_capital < 0:
        raise ValueError("available_capital cannot be negative")

    delegated = sum(
        record.delegated_capacity
        for record in registry.by_delegator(delegator_id)
    )

    return available_capital - delegated
