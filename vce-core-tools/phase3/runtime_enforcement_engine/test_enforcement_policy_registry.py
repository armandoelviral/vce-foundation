from phase3.runtime_enforcement_engine.enforcement_policy_record import (
    EnforcementPolicyRecord,
)

from phase3.runtime_enforcement_engine.enforcement_policy_registry import (
    EnforcementPolicyRegistry,
)


def test_registry_starts_empty():

    registry = EnforcementPolicyRegistry()

    assert registry.count() == 0


def test_registry_accepts_policy():

    registry = EnforcementPolicyRegistry()

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    registry.add(
        policy
    )

    assert registry.count() == 1


def test_registry_returns_policy():

    registry = EnforcementPolicyRegistry()

    policy = EnforcementPolicyRecord(
        policy_id="policy-001",
        policy_name="default_enforcement",
    )

    registry.add(
        policy
    )

    recovered = registry.get(
        "policy-001"
    )

    assert recovered == policy


def test_missing_policy_returns_none():

    registry = EnforcementPolicyRegistry()

    assert registry.get(
        "missing"
    ) is None
