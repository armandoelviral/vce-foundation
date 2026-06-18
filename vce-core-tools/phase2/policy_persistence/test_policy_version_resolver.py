from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_store import (
    PolicyStore,
)

from phase2.policy_persistence.policy_version_resolver import (
    PolicyVersionResolver,
)


def test_resolver_returns_latest_version():

    store = PolicyStore()

    store.add(
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="rule-v1",
        )
    )

    store.add(
        PolicyRecord(
            policy_id="policy-001",
            version=2,
            rule="rule-v2",
        )
    )

    resolver = PolicyVersionResolver(
        store
    )

    result = resolver.latest(
        "policy-001"
    )

    assert result.version == 2


def test_resolver_returns_single_version():

    store = PolicyStore()

    store.add(
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="rule-v1",
        )
    )

    resolver = PolicyVersionResolver(
        store
    )

    result = resolver.latest(
        "policy-001"
    )

    assert result.version == 1


def test_resolver_returns_none_for_missing_policy():

    store = PolicyStore()

    resolver = PolicyVersionResolver(
        store
    )

    assert (
        resolver.latest(
            "missing"
        )
        is None
    )
