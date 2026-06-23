from epics.phase4_027_delegation_economy.delegation_audit import (
    audit_active_delegations,
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


def test_audit_returns_active_delegations():
    registry = DelegationRegistry()

    active = DelegationRecord(
        delegation_id="delegation.active",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="active",
    )

    registry.add(active)

    audit = audit_active_delegations(
        registry=registry,
        revocations=[],
    )

    assert audit["active_count"] == 1
    assert audit["active_delegations"] == [active]


def test_revoked_delegation_is_removed_from_active_set():
    registry = DelegationRegistry()

    active = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="active",
    )

    registry.add(active)

    revocation = DelegationRevocationRecord(
        revocation_id="revocation.001",
        delegation_id="delegation.001",
        reason="revoked",
    )

    audit = audit_active_delegations(
        registry=registry,
        revocations=[revocation],
    )

    assert audit["active_count"] == 0
    assert audit["active_delegations"] == []


def test_partial_revocation_keeps_other_delegations_active():
    registry = DelegationRegistry()

    first = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="first",
    )

    second = DelegationRecord(
        delegation_id="delegation.002",
        delegator_id="institution.alpha",
        delegate_id="citizen.gamma",
        delegated_capacity=50,
        reason="second",
    )

    registry.add(first)
    registry.add(second)

    revocation = DelegationRevocationRecord(
        revocation_id="revocation.001",
        delegation_id="delegation.001",
        reason="revoked",
    )

    audit = audit_active_delegations(
        registry=registry,
        revocations=[revocation],
    )

    assert audit["active_count"] == 1
    assert audit["active_delegations"] == [second]
