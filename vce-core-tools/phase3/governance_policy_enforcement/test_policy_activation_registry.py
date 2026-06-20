from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)

from phase3.governance_policy_enforcement.policy_activation_registry import (
    PolicyActivationRegistry,
)


def test_registry_starts_empty():

    registry = PolicyActivationRegistry()

    assert registry.count() == 0


def test_registry_accepts_activation():

    registry = PolicyActivationRegistry()

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_returns_activation():

    registry = PolicyActivationRegistry()

    record = PolicyActivationRecord(
        activation_id="activation-001",
        policy_id="policy-001",
        status="ACTIVE",
    )

    registry.add(record)

    recovered = registry.get(
        "activation-001"
    )

    assert recovered == record


def test_missing_activation_returns_none():

    registry = PolicyActivationRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_activation_ids():

    registry = PolicyActivationRegistry()

    registry.add(
        PolicyActivationRecord(
            activation_id="activation-001",
            policy_id="policy-001",
            status="ACTIVE",
        )
    )

    registry.add(
        PolicyActivationRecord(
            activation_id="activation-002",
            policy_id="policy-002",
            status="INACTIVE",
        )
    )

    assert registry.activation_ids() == [
        "activation-001",
        "activation-002",
    ]
