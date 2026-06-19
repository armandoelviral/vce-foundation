from phase3.governance_recovery.reinstatement_decision import (
    ReinstatementDecision,
)


def test_reinstate_decision():

    decision = (
        ReinstatementDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "REINSTATE"
    )


def test_reject_reinstatement_decision():

    decision = (
        ReinstatementDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_REINSTATEMENT"
    )


def test_decision_serializes():

    decision = (
        ReinstatementDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "REINSTATE"
    }
