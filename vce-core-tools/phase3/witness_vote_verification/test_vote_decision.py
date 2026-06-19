from phase3.witness_vote_verification.vote_decision import (
    VoteDecision,
)


def test_accept_vote():

    decision = VoteDecision.from_verification(
        True
    )

    assert (
        decision.status
        == "ACCEPT_VOTE"
    )


def test_reject_vote():

    decision = VoteDecision.from_verification(
        False
    )

    assert (
        decision.status
        == "REJECT_VOTE"
    )


def test_decision_serializes():

    decision = VoteDecision.from_verification(
        True
    )

    assert decision.to_dict() == {
        "status": "ACCEPT_VOTE"
    }
