from phase2.witness_persistence.witness_vote_record import (
    WitnessVoteRecord,
)

from phase2.witness_persistence.witness_vote_store import (
    WitnessVoteStore,
)


def test_store_starts_empty():

    store = WitnessVoteStore()

    assert store.count() == 0


def test_store_accepts_vote():

    store = WitnessVoteStore()

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    store.add(vote)

    assert store.count() == 1


def test_store_returns_vote():

    store = WitnessVoteStore()

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    store.add(vote)

    recovered = store.get(
        "witness-001",
        "decision-001",
    )

    assert recovered == vote


def test_unknown_vote_returns_none():

    store = WitnessVoteStore()

    assert store.get(
        "missing",
        "decision-001",
    ) is None
