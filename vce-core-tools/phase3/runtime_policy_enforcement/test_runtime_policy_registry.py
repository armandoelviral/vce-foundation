from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_registry import (
    RuntimePolicyRegistry,
)


def test_registry_starts_empty():

    registry = RuntimePolicyRegistry()

    assert registry.count() == 0


def test_registry_accepts_policy():

    registry = RuntimePolicyRegistry()

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    registry.add(policy)

    assert registry.count() == 1


def test_registry_returns_policy():

    registry = RuntimePolicyRegistry()

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    registry.add(policy)

    recovered = registry.get(
        "policy-001"
    )

    assert recovered == policy


def test_missing_policy_returns_none():

    registry = RuntimePolicyRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_policy_ids():

    registry = RuntimePolicyRegistry()

    registry.add(
        RuntimePolicyRecord(
            policy_id="policy-001",
            resource_type="REPLAY",
            action="EXECUTE",
            effect="ALLOW",
        )
    )

    registry.add(
        RuntimePolicyRecord(
            policy_id="policy-002",
            resource_type="WITNESS",
            action="PARTICIPATE",
            effect="DENY",
        )
    )

    assert registry.policy_ids() == [
        "policy-001",
        "policy-002",
    ]
