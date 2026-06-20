from phase3.runtime_policy_enforcement.runtime_policy_record import (
    RuntimePolicyRecord,
)

from phase3.runtime_policy_enforcement.runtime_policy_registry import (
    RuntimePolicyRegistry,
)

from phase3.runtime_policy_enforcement.runtime_policy_query import (
    RuntimePolicyQuery,
)


def test_query_returns_policy():

    registry = RuntimePolicyRegistry()

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    registry.add(policy)

    query = RuntimePolicyQuery(
        registry
    )

    result = query.by_id(
        "policy-001"
    )

    assert result == policy


def test_query_returns_none_for_missing():

    registry = RuntimePolicyRegistry()

    query = RuntimePolicyQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_effect():

    registry = RuntimePolicyRegistry()

    policy = RuntimePolicyRecord(
        policy_id="policy-001",
        resource_type="REPLAY",
        action="EXECUTE",
        effect="ALLOW",
    )

    registry.add(policy)

    query = RuntimePolicyQuery(
        registry
    )

    result = query.by_id(
        "policy-001"
    )

    assert result.effect == "ALLOW"
