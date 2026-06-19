from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)

from phase3.witness_vote_verification.vote_verification import (
    VoteVerification,
)


def test_approve_vote_is_valid():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is True
    )


def test_reject_vote_is_valid():

    vote = WitnessVoteRecord(
        vote_id="vote-002",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="REJECT",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is True
    )


def test_abstain_vote_is_valid():

    vote = WitnessVoteRecord(
        vote_id="vote-003",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="ABSTAIN",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is True
    )


def test_missing_vote_id_fails():

    vote = WitnessVoteRecord(
        vote_id="",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is False
    )


def test_missing_witness_did_fails():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="",
        vote_value="APPROVE",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is False
    )


def test_invalid_vote_value_fails():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="INVALID",
    )

    assert (
        VoteVerification.verify(
            vote
        )
        is False
    )
