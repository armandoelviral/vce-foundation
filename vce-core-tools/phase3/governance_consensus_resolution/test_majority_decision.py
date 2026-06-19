from phase3.governance_consensus_resolution.majority_decision import (
    MajorityDecision,
)


def test_approved_when_approve_votes_win():

    outcome = MajorityDecision.decide(
        approve_votes=3,
        reject_votes=1,
    )

    assert outcome == "APPROVED"


def test_rejected_when_reject_votes_win():

    outcome = MajorityDecision.decide(
        approve_votes=1,
        reject_votes=3,
    )

    assert outcome == "REJECTED"


def test_rejected_when_tied():

    outcome = MajorityDecision.decide(
        approve_votes=2,
        reject_votes=2,
    )

    assert outcome == "REJECTED"


def test_rejected_when_no_votes():

    outcome = MajorityDecision.decide(
        approve_votes=0,
        reject_votes=0,
    )

    assert outcome == "REJECTED"
