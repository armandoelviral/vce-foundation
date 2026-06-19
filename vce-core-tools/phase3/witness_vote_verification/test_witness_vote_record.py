from phase3.witness_vote_verification.witness_vote_record import (
    WitnessVoteRecord,
)


def test_contains_vote_id():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert vote.vote_id == "vote-001"


def test_contains_witness_did():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert (
        vote.witness_did
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_contains_vote_value():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert vote.vote_value == "APPROVE"


def test_serializes():

    vote = WitnessVoteRecord(
        vote_id="vote-001",
        witness_did="did:vcr:gcp:us-central1:fp001",
        vote_value="APPROVE",
    )

    assert vote.to_dict() == {
        "vote_id": "vote-001",
        "witness_did":
            "did:vcr:gcp:us-central1:fp001",
        "vote_value": "APPROVE",
    }
