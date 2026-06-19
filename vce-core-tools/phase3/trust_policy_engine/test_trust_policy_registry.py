from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)

from phase3.trust_policy_engine.trust_policy_registry import (
    TrustPolicyRegistry,
)


def test_registry_starts_empty():

    registry = TrustPolicyRegistry()

    assert registry.count() == 0


def test_registry_accepts_policy():

    registry = TrustPolicyRegistry()

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    registry.add(policy)

    assert registry.count() == 1


def test_registry_returns_policy():

    registry = TrustPolicyRegistry()

    policy = TrustPolicyRecord(
        policy_id="policy-001",
        policy_name="default_trust",
    )

    registry.add(policy)

    recovered = registry.get(
        "policy-001"
    )

    assert recovered == policy


def test_missing_policy_returns_none():

    registry = TrustPolicyRegistry()

    assert registry.get(
        "missing"
    ) is None
