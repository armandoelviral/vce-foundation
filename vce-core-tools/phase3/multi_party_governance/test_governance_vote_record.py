from phase3.multi_party_governance.governance_vote_record import (
    GovernanceVoteRecord,
)


def test_vote_contains_id():

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    assert vote.vote_id == "vote-001"


def test_vote_contains_voter():

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    assert vote.voter_id == "witness-001"


def test_vote_contains_decision():

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    assert vote.vote == "APPROVE"


def test_vote_serializes():

    vote = GovernanceVoteRecord(
        vote_id="vote-001",
        voter_id="witness-001",
        vote="APPROVE",
    )

    assert vote.to_dict() == {
        "vote_id": "vote-001",
        "voter_id": "witness-001",
        "vote": "APPROVE",
    }
