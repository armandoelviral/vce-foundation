from phase2.witness_persistence.witness_vote_record import (
    WitnessVoteRecord,
)

from phase2.witness_persistence.witness_vote_store import (
    WitnessVoteStore,
)

from phase2.witness_persistence.witness_vote_query import (
    WitnessVoteQuery,
)


def test_query_returns_votes_by_decision():

    store = WitnessVoteStore()

    store.add(
        WitnessVoteRecord(
            witness_id="witness-001",
            decision_id="decision-001",
            vote=True,
        )
    )

    query = WitnessVoteQuery(store)

    results = query.by_decision(
        "decision-001"
    )

    assert len(results) == 1
    assert results[0].witness_id == "witness-001"


def test_query_returns_empty_for_unknown_decision():

    store = WitnessVoteStore()

    query = WitnessVoteQuery(store)

    assert query.by_decision(
        "missing"
    ) == []


def test_query_filters_multiple_decisions():

    store = WitnessVoteStore()

    store.add(
        WitnessVoteRecord(
            witness_id="witness-001",
            decision_id="decision-001",
            vote=True,
        )
    )

    store.add(
        WitnessVoteRecord(
            witness_id="witness-002",
            decision_id="decision-002",
            vote=False,
        )
    )

    query = WitnessVoteQuery(store)

    results = query.by_decision(
        "decision-002"
    )

    assert len(results) == 1
    assert results[0].witness_id == "witness-002"
