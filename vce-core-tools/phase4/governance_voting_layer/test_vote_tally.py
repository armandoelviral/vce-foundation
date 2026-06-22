from phase4.governance_voting_layer.vote_tally import (
    VoteTally,
)

from phase4.governance_voting_layer.vote_record import (
    VoteRecord,
)


def test_counts_yes_votes():

    votes = [
        VoteRecord(
            citizen_did="a",
            proposal_id="proposal-001",
            vote="YES",
        ),
        VoteRecord(
            citizen_did="b",
            proposal_id="proposal-001",
            vote="YES",
        ),
        VoteRecord(
            citizen_did="c",
            proposal_id="proposal-001",
            vote="NO",
        ),
    ]

    tally = VoteTally.calculate(
        proposal_id="proposal-001",
        votes=votes,
    )

    assert tally["yes_votes"] == 2


def test_counts_no_votes():

    votes = [
        VoteRecord(
            citizen_did="a",
            proposal_id="proposal-001",
            vote="YES",
        ),
        VoteRecord(
            citizen_did="b",
            proposal_id="proposal-001",
            vote="NO",
        ),
        VoteRecord(
            citizen_did="c",
            proposal_id="proposal-001",
            vote="NO",
        ),
    ]

    tally = VoteTally.calculate(
        proposal_id="proposal-001",
        votes=votes,
    )

    assert tally["no_votes"] == 2


def test_serializes():

    votes = [
        VoteRecord(
            citizen_did="a",
            proposal_id="proposal-001",
            vote="YES",
        ),
    ]

    tally = VoteTally.calculate(
        proposal_id="proposal-001",
        votes=votes,
    )

    assert tally == {
        "proposal_id": "proposal-001",
        "yes_votes": 1,
        "no_votes": 0,
    }
