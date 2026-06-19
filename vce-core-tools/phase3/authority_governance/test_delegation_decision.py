from phase3.authority_governance.delegation_decision import (
    DelegationDecision,
)


def test_delegate_decision():

    decision = (
        DelegationDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "DELEGATE"
    )


def test_deny_decision():

    decision = (
        DelegationDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "DENY"
    )


def test_decision_serializes():

    decision = (
        DelegationDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "DELEGATE"
    }
