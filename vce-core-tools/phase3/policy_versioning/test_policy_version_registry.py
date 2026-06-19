from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)

from phase3.policy_versioning.policy_version_registry import (
    PolicyVersionRegistry,
)


def test_registry_starts_empty():

    registry = PolicyVersionRegistry()

    assert registry.count() == 0


def test_registry_accepts_record():

    registry = PolicyVersionRegistry()

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    registry.add(record)

    assert registry.count() == 1


def test_registry_returns_record():

    registry = PolicyVersionRegistry()

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    registry.add(record)

    recovered = registry.get(
        "trust-policy:v1"
    )

    assert recovered == record


def test_missing_record_returns_none():

    registry = PolicyVersionRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_versions():

    registry = PolicyVersionRegistry()

    registry.add(
        PolicyVersionRecord(
            policy_id="trust-policy",
            version="v1",
            approved_by="auth-001",
        )
    )

    registry.add(
        PolicyVersionRecord(
            policy_id="trust-policy",
            version="v2",
            approved_by="auth-001",
        )
    )

    assert registry.version_ids() == [
        "trust-policy:v1",
        "trust-policy:v2",
    ]
