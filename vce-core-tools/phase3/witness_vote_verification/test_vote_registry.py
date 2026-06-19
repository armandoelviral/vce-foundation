from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_registry import (
    VoteRegistry,
)


def test_registry_starts_empty():

    registry = VoteRegistry()

    assert registry.count() == 0


def test_registry_accepts_vote():

    registry = VoteRegistry()

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    registry.add(vote)

    assert registry.count() == 1


def test_registry_returns_vote():

    registry = VoteRegistry()

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    registry.add(vote)

    recovered = registry.get(
        "vote-001"
    )

    assert recovered == vote


def test_missing_vote_returns_none():

    registry = VoteRegistry()

    assert registry.get(
        "missing"
    ) is None


def test_registry_lists_vote_ids():

    registry = VoteRegistry()

    registry.add(
        WitnessVoteRecord(
            vote_id="vote-001",
            witness_did="did:vcr:gcp:us-central1:fp001",
            vote_value="APPROVE",
        )
    )

    registry.add(
        WitnessVoteRecord(
            vote_id="vote-002",
            witness_did="did:vcr:aws:us-east-1:fp002",
            vote_value="REJECT",
        )
    )

    assert registry.vote_ids() == [
        "vote-001",
        "vote-002",
    ]
