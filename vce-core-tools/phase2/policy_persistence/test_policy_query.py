from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_store import (
    PolicyStore,
)

from phase2.policy_persistence.policy_query import (
    PolicyQuery,
)


def test_query_returns_policy_by_id():

    store = PolicyStore()

    store.add(
        PolicyRecord(
            policy_id="policy-001",
            version=1,
            rule="allow_signed_artifacts_only",
        )
    )

    query = PolicyQuery(store)

    result = query.by_id(
        "policy-001",
        1,
    )

    assert result.policy_id == "policy-001"


def test_query_returns_none_for_missing_policy():

    store = PolicyStore()

    query = PolicyQuery(store)

    assert query.by_id(
        "missing",
        1,
    ) is None


def test_query_returns_correct_version():

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

    query = PolicyQuery(store)

    result = query.by_id(
        "policy-001",
        2,
    )

    assert result.rule == "rule-v2"
