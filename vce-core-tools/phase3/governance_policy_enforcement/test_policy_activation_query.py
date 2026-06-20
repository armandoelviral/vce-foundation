from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_registry import (
    PolicyActivationRegistry,
)

from phase3.governance_policy_enforcement.policy_activation_query import (
    PolicyActivationQuery,
)


def test_query_returns_activation():

    registry = PolicyActivationRegistry()

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    registry.add(record)

    query = PolicyActivationQuery(
        registry
    )

    result = query.by_id(
        "activation-001"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = PolicyActivationRegistry()

    query = PolicyActivationQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_status():

    registry = PolicyActivationRegistry()

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    registry.add(record)

    query = PolicyActivationQuery(
        registry
    )

    result = query.by_id(
        "activation-001"
    )

    assert result.status == "ACTIVE"
