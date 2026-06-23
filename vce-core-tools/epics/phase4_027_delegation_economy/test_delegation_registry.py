from epics.phase4_027_delegation_economy.delegation_record import (
    DelegationRecord,
)
from epics.phase4_027_delegation_economy.delegation_registry import (
    DelegationRegistry,
)


def test_registry_stores_delegation():
    registry = DelegationRegistry()

    record = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="constitutional sponsorship",
    )

    registry.add(record)

    records = registry.records()

    assert len(records) == 1
    assert records[0] == record


def test_registry_rejects_duplicate_delegation_id():
    registry = DelegationRegistry()

    first = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="first",
    )

    second = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.gamma",
        delegate_id="citizen.delta",
        delegated_capacity=50,
        reason="second",
    )

    registry.add(first)

    try:
        registry.add(second)
        assert False
    except ValueError as exc:
        assert "duplicate delegation" in str(exc)


def test_registry_returns_copy():
    registry = DelegationRegistry()

    record = DelegationRecord(
        delegation_id="delegation.001",
        delegator_id="institution.alpha",
        delegate_id="citizen.beta",
        delegated_capacity=25,
        reason="delegation",
    )

    registry.add(record)

    records = registry.records()

    records.clear()

    assert len(registry.records()) == 1


def test_registry_can_filter_by_delegator():
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
            delegator_id="institution.gamma",
            delegate_id="citizen.delta",
            delegated_capacity=50,
            reason="delegation",
        )
    )

    results = registry.by_delegator("institution.alpha")

    assert len(results) == 1
    assert results[0].delegation_id == "delegation.001"
