from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)

from phase3.policy_versioning.policy_version_registry import (
    PolicyVersionRegistry,
)

from phase3.policy_versioning.policy_version_query import (
    PolicyVersionQuery,
)


def test_query_returns_version():

    registry = PolicyVersionRegistry()

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    registry.add(record)

    query = PolicyVersionQuery(
        registry
    )

    result = query.by_id(
        "trust-policy:v1"
    )

    assert result == record


def test_query_returns_none_for_missing():

    registry = PolicyVersionRegistry()

    query = PolicyVersionQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_version_number():

    registry = PolicyVersionRegistry()

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    registry.add(record)

    query = PolicyVersionQuery(
        registry
    )

    result = query.by_id(
        "trust-policy:v1"
    )

    assert result.version == "v1"
