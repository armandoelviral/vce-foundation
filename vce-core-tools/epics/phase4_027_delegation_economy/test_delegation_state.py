from epics.phase4_027_delegation_economy.delegation_state import (
    DelegationState,
)
from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)
from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)
from epics.phase4_027_delegation_economy.delegation_revocation import (
    DelegationRevocationRecord,
)


def test_builds_delegation_state():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="delegation",
        )
    )

    registry.add(
        DelegationRecord(
            delegation_id="delegation.002",
            delegator_id="institution.alpha",
            delegate_id="citizen.gamma",
            delegated_capacity=15,
            reason="delegation",
        )
    )

    state = DelegationState.from_records(
        registry=registry,
        revocations=[],
        delegator_id="institution.alpha",
    )

    assert state.delegator_id == "institution.alpha"
    assert state.active_delegations == 2
    assert state.total_delegated_capacity == 40


def test_revoked_delegation_not_counted():
    registry = DelegationRegistry()

    registry.add(
        DelegationRecord(
            delegation_id="delegation.001",
            delegator_id="institution.alpha",
            delegate_id="citizen.beta",
            delegated_capacity=25,
            reason="delegation",
        )
    )

    revocation = DelegationRevocationRecord(
        revocation_id="revocation.001",
        delegation_id="delegation.001",
        reason="revoked",
    )

    state = DelegationState.from_records(
        registry=registry,
        revocations=[revocation],
        delegator_id="institution.alpha",
    )

    assert state.active_delegations == 0
    assert state.total_delegated_capacity == 0


def test_unknown_delegator_has_empty_state():
    registry = DelegationRegistry()

    state = DelegationState.from_records(
        registry=registry,
        revocations=[],
        delegator_id="institution.unknown",
    )

    assert state.active_delegations == 0
    assert state.total_delegated_capacity == 0
