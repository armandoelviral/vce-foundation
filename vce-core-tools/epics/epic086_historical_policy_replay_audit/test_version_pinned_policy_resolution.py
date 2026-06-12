from epics.epic085_policy_authority_layer.policy_registry import (
    GovernancePolicy,
    PolicyRegistry,
)
from epics.epic086_historical_policy_replay_audit.version_pinned_policy_resolution import (
    VersionPinnedPolicyResolution,
)


def build_registry():

    registry = PolicyRegistry()

    registry.register(
        GovernancePolicy(
            policy_id="clinical-admission-policy",
            policy_version="1.0.0",
            policy_hash="policy-hash-v1",
            active=True,
        )
    )

    registry.register(
        GovernancePolicy(
            policy_id="clinical-admission-policy",
            policy_version="2.0.0",
            policy_hash="policy-hash-v2",
            active=True,
        )
    )

    return registry


def test_resolution_returns_exact_policy_version():

    resolver = VersionPinnedPolicyResolution(
        build_registry()
    )

    policy = resolver.resolve(
        "clinical-admission-policy",
        "2.0.0",
    )

    assert policy.policy_version == "2.0.0"
    assert policy.policy_hash == "policy-hash-v2"


def test_resolution_does_not_return_latest_by_default():

    resolver = VersionPinnedPolicyResolution(
        build_registry()
    )

    policy = resolver.resolve(
        "clinical-admission-policy",
        "1.0.0",
    )

    assert policy.policy_version == "1.0.0"
    assert policy.policy_hash == "policy-hash-v1"


def test_resolution_returns_none_for_unknown_version():

    resolver = VersionPinnedPolicyResolution(
        build_registry()
    )

    assert (
        resolver.resolve(
            "clinical-admission-policy",
            "9.9.9",
        )
        is None
    )
