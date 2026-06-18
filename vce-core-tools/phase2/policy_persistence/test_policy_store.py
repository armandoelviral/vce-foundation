from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_store import (
    PolicyStore,
)


def test_store_starts_empty():

    store = PolicyStore()

    assert store.count() == 0


def test_store_accepts_policy():

    store = PolicyStore()

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    store.add(record)

    assert store.count() == 1


def test_store_returns_policy_by_id():

    store = PolicyStore()

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    store.add(record)

    recovered = store.get(
        "policy-001",
        1,
    )

    assert recovered == record


def test_unknown_policy_returns_none():

    store = PolicyStore()

    assert store.get(
        "missing",
        1,
    ) is None
