from phase4.governance_voting_layer.vote_record import (
    VoteRecord,
)


def test_contains_did():

    vote = VoteRecord(
        citizen_did="did:tcn:test:01",
        proposal_id="proposal-001",
        vote="YES",
    )

    assert vote.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_proposal():

    vote = VoteRecord(
        citizen_did="did:tcn:test:01",
        proposal_id="proposal-001",
        vote="YES",
    )

    assert vote.proposal_id == (
        "proposal-001"
    )


def test_contains_vote():

    vote = VoteRecord(
        citizen_did="did:tcn:test:01",
        proposal_id="proposal-001",
        vote="YES",
    )

    assert vote.vote == "YES"


def test_serializes():

    vote = VoteRecord(
        citizen_did="did:tcn:test:01",
        proposal_id="proposal-001",
        vote="YES",
    )

    assert vote.to_dict() == {
        "citizen_did":
            "did:tcn:test:01",
        "proposal_id":
            "proposal-001",
        "vote":
            "YES",
    }
