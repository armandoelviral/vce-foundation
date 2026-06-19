from phase3.runtime_governance.governance_decision import (
    GovernanceDecision,
)


def test_approved_decision():

    decision = (
        GovernanceDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "APPROVED"
    )


def test_rejected_decision():

    decision = (
        GovernanceDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECTED"
    )


def test_decision_serializes():

    decision = (
        GovernanceDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "APPROVED"
    }
