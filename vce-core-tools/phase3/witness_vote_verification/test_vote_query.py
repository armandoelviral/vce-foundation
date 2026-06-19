from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_registry import (
    VoteRegistry,
)

from phase3.witness_vote_verification.vote_query import (
    VoteQuery,
)


def test_query_returns_vote():

    registry = VoteRegistry()

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    registry.add(vote)

    query = VoteQuery(
        registry
    )

    result = query.by_id(
        "vote-001"
    )

    assert result == vote


def test_query_returns_none_for_missing():

    registry = VoteRegistry()

    query = VoteQuery(
        registry
    )

    assert query.by_id(
        "missing"
    ) is None


def test_query_returns_vote_value():

    registry = VoteRegistry()

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    registry.add(vote)

    query = VoteQuery(
        registry
    )

    result = query.by_id(
        "vote-001"
    )

    assert (
        result.vote_value
        == "APPROVE"
    )
