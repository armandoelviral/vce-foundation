from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)

from phase2.policy_persistence.policy_store import (
    PolicyStore,
)

from phase2.policy_persistence.policy_query import (
    PolicyQuery,
)

from phase2.policy_persistence.policy_version_resolver import (
    PolicyVersionResolver,
)

from phase2.policy_persistence.policy_replay_binding import (
    PolicyReplayBinding,
)

from phase2.policy_persistence.policy_verifier import (
    PolicyVerifier,
)

from phase2.policy_persistence.policy_report import (
    PolicyReport,
)


def test_end_to_end_policy_persistence_flow():

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

    policy = query.by_id(
        "policy-001",
        2,
    )

    assert policy.version == 2

    resolver = PolicyVersionResolver(
        store
    )

    latest = resolver.latest(
        "policy-001"
    )

    assert latest.version == 2

    binding = PolicyReplayBinding(
        policy_id="policy-001",
        version=2,
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100

    verified = PolicyVerifier.verify(
        latest,
        expected_version=2,
    )

    assert verified is True

    report = PolicyReport(
        [latest]
    )

    assert (
        report.total_policies()
        == 1
    )

    assert report.policy_ids() == [
        "policy-001"
    ]
