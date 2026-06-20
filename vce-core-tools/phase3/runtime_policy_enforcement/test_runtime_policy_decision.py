from phase3.runtime_policy_enforcement.runtime_policy_decision import (
    RuntimePolicyDecision,
)


def test_allow_request():

    decision = (
        RuntimePolicyDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "ALLOW_REQUEST"
    )


def test_deny_request():

    decision = (
        RuntimePolicyDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "DENY_REQUEST"
    )


def test_decision_serializes():

    decision = (
        RuntimePolicyDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status":
            "ALLOW_REQUEST"
    }
