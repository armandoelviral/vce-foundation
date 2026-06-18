from phase2.witness_persistence.consensus_decision_record import (
    ConsensusDecisionRecord,
)


def test_decision_contains_id():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=3,
    )

    assert decision.decision_id == "decision-001"


def test_decision_contains_approval_status():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=3,
    )

    assert decision.approved is True


def test_decision_contains_vote_count():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=3,
    )

    assert decision.vote_count == 3


def test_decision_serializes():

    decision = ConsensusDecisionRecord(
        decision_id="decision-001",
        approved=True,
        vote_count=3,
    )

    assert decision.to_dict() == {
        "decision_id": "decision-001",
        "approved": True,
        "vote_count": 3,
    }
