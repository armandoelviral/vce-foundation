from phase3.governance_escalation.suspension_decision import (
    SuspensionDecision,
)


def test_suspend_decision():

    decision = SuspensionDecision.from_evaluation(
        True
    )

    assert decision.status == "SUSPEND"


def test_continue_decision():

    decision = SuspensionDecision.from_evaluation(
        False
    )

    assert decision.status == "CONTINUE"


def test_decision_serializes():

    decision = SuspensionDecision.from_evaluation(
        True
    )

    assert decision.to_dict() == {
        "status": "SUSPEND"
    }
