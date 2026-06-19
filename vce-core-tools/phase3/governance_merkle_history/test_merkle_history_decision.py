from phase3.governance_merkle_history.merkle_history_decision import (
    MerkleHistoryDecision,
)


def test_accept_merkle():

    decision = (
        MerkleHistoryDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "ACCEPT_MERKLE"
    )


def test_reject_merkle():

    decision = (
        MerkleHistoryDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_MERKLE"
    )


def test_decision_serializes():

    decision = (
        MerkleHistoryDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "ACCEPT_MERKLE"
    }
