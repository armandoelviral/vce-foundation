from phase2.witness_persistence.witness_vote_record import (
    WitnessVoteRecord,
)


def test_vote_contains_witness_id():

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    assert vote.witness_id == "witness-001"


def test_vote_contains_decision_id():

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    assert vote.decision_id == "decision-001"


def test_vote_contains_vote_value():

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    assert vote.vote is True


def test_vote_serializes():

    vote = WitnessVoteRecord(
        witness_id="witness-001",
        decision_id="decision-001",
        vote=True,
    )

    assert vote.to_dict() == {
        "witness_id": "witness-001",
        "decision_id": "decision-001",
        "vote": True,
    }
