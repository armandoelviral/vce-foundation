from phase3.admission_control_engine.admission_decision import (
    AdmissionDecision,
)


def test_allow_decision():

    decision = AdmissionDecision.from_evaluation(
        True
    )

    assert decision.status == "ALLOW"


def test_deny_decision():

    decision = AdmissionDecision.from_evaluation(
        False
    )

    assert decision.status == "DENY"


def test_decision_serializes():

    decision = AdmissionDecision.from_evaluation(
        True
    )

    assert decision.to_dict() == {
        "status": "ALLOW"
    }
