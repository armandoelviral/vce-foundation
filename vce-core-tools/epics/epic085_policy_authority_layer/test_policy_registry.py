from epics.epic085_policy_authority_layer.policy_registry import (
    GovernancePolicy,
    PolicyRegistry,
)


def build_registry():

    registry = PolicyRegistry()

    registry.register(
        GovernancePolicy(
            policy_id="clinical-admission-policy",
            policy_version="1.0.0",
            policy_hash="policy-hash-001",
            active=True,
        )
    )

    return registry


def test_policy_registry_registers_policy():

    registry = build_registry()

    policy = registry.get(
        "clinical-admission-policy",
        "1.0.0",
    )

    assert policy is not None


def test_policy_registry_returns_policy_metadata():

    registry = build_registry()

    policy = registry.get(
        "clinical-admission-policy",
        "1.0.0",
    )

    assert policy.policy_hash == "policy-hash-001"


def test_policy_registry_accepts_active_policy():

    registry = build_registry()

    assert (
        registry.is_registered(
            "clinical-admission-policy",
            "1.0.0",
        )
        is True
    )


def test_policy_registry_rejects_unknown_policy():

    registry = build_registry()

    assert (
        registry.is_registered(
            "unknown-policy",
            "1.0.0",
        )
        is False
    )


def test_policy_registry_rejects_inactive_policy():

    registry = PolicyRegistry()

    registry.register(
        GovernancePolicy(
            policy_id="deprecated-policy",
            policy_version="1.0.0",
            policy_hash="policy-hash-999",
            active=False,
        )
    )

    assert (
        registry.is_registered(
            "deprecated-policy",
            "1.0.0",
        )
        is False
    )
