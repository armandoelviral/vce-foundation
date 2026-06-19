from phase3.hybrid_signature_verification.signature_decision import (
    SignatureDecision,
)


def test_accept_signature():

    decision = (
        SignatureDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "ACCEPT_SIGNATURE"
    )


def test_reject_signature():

    decision = (
        SignatureDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_SIGNATURE"
    )


def test_decision_serializes():

    decision = (
        SignatureDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status":
            "ACCEPT_SIGNATURE"
    }
