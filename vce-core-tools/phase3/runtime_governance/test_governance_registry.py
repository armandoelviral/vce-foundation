from phase3.runtime_governance.governance_policy_record import (
    GovernancePolicyRecord,
)

from phase3.runtime_governance.governance_registry import (
    GovernanceRegistry,
)


def test_registry_starts_empty():

    registry = GovernanceRegistry()

    assert registry.count() == 0


def test_registry_accepts_policy():

    registry = GovernanceRegistry()

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    registry.add(policy)

    assert registry.count() == 1


def test_registry_returns_policy():

    registry = GovernanceRegistry()

    policy = GovernancePolicyRecord(
        policy_id="policy-001",
        policy_name="default_governance",
    )

    registry.add(policy)

    recovered = registry.get(
        "policy-001"
    )

    assert recovered == policy


def test_missing_policy_returns_none():

    registry = GovernanceRegistry()

    assert registry.get(
        "missing"
    ) is None
