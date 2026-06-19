from phase3.governance_inclusion_proof.proof_decision import (
    ProofDecision,
)


def test_accept_proof():

    decision = ProofDecision.from_evaluation(
        True
    )

    assert decision.status == "ACCEPT_PROOF"


def test_reject_proof():

    decision = ProofDecision.from_evaluation(
        False
    )

    assert decision.status == "REJECT_PROOF"


def test_decision_serializes():

    decision = ProofDecision.from_evaluation(
        True
    )

    assert decision.to_dict() == {
        "status": "ACCEPT_PROOF"
    }
