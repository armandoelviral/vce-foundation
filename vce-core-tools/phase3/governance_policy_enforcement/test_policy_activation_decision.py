from phase3.governance_policy_enforcement.policy_activation_decision import (
    PolicyActivationDecision,
)


def test_activate_policy():

    decision = (
        PolicyActivationDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "ACTIVATE_POLICY"
    )


def test_do_not_activate_policy():

    decision = (
        PolicyActivationDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "DO_NOT_ACTIVATE"
    )


def test_decision_serializes():

    decision = (
        PolicyActivationDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status":
            "ACTIVATE_POLICY"
    }
