from phase4.trusted_compute_network_governance.admission_decision import (
    AdmissionDecision,
)


def test_contains_proposal_id():

    decision = AdmissionDecision(
        proposal_id="proposal-001",
        approved=True,
        vote_count=3,
    )

    assert decision.proposal_id == "proposal-001"


def test_contains_decision():

    decision = AdmissionDecision(
        proposal_id="proposal-001",
        approved=True,
        vote_count=3,
    )

    assert decision.approved is True


def test_contains_vote_count():

    decision = AdmissionDecision(
        proposal_id="proposal-001",
        approved=True,
        vote_count=3,
    )

    assert decision.vote_count == 3


def test_serializes():

    decision = AdmissionDecision(
        proposal_id="proposal-001",
        approved=True,
        vote_count=3,
    )

    assert decision.to_dict() == {
        "proposal_id": "proposal-001",
        "approved": True,
        "vote_count": 3,
    }
