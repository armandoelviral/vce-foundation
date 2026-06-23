from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)
from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)
from epics.phase4_027_delegation_economy.delegation_revocation import (
    DelegationRevocationRecord,
)
from epics.phase4_027_delegation_economy.delegation_state import (
    DelegationState,
)
from epics.phase4_027_delegation_economy.delegation_verifier import (
    verify_delegation_state,
)


def test_end_to_end_delegation_flow():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=30,
            reason="constitutional sponsorship",
        )
    )

    registry.add(
        DelegationRecord(
            delegation_id="delegation.002",
            delegator_id="institution.alpha",
            delegate_id="citizen.gamma",
            delegated_capacity=20,
            reason="institutional backing",
        )
    )

    revocation = DelegationRevocationRecord(
        revocation_id="revocation.001",
        delegation_id="delegation.001",
        reason="expired authority",
    )

    state = DelegationState.from_records(
        registry=registry,
        revocations=[revocation],
        delegator_id="institution.alpha",
    )

    assert state.active_delegations == 1
    assert state.total_delegated_capacity == 20

    verification = verify_delegation_state(
        state=state,
        available_capital=100,
    )

    assert verification["verified"] is True
    assert verification["remaining_capacity"] == 80
