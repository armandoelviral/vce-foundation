from phase4.governance_voting_layer.consensus_decision import (
    ConsensusDecision,
)


def test_approves_when_yes_majority():

    tally = {
        "proposal_id": "proposal-001",
        "yes_votes": 3,
        "no_votes": 1,
    }

    result = ConsensusDecision.decide(
        tally
    )

    assert result["decision"] == (
        "APPROVED"
    )


def test_rejects_when_no_majority():

    tally = {
        "proposal_id": "proposal-001",
        "yes_votes": 1,
        "no_votes": 3,
    }

    result = ConsensusDecision.decide(
        tally
    )

    assert result["decision"] == (
        "REJECTED"
    )


def test_rejects_when_tied():

    tally = {
        "proposal_id": "proposal-001",
        "yes_votes": 2,
        "no_votes": 2,
    }

    result = ConsensusDecision.decide(
        tally
    )

    assert result["decision"] == (
        "REJECTED"
    )
