from phase3.governance_policy_enforcement.policy_activation_evaluation import (
    PolicyActivationEvaluation,
)


def test_approved_consensus_activates():

    assert (
        PolicyActivationEvaluation.evaluate(
            "APPROVED"
        )
        is True
    )


def test_rejected_consensus_fails():

    assert (
        PolicyActivationEvaluation.evaluate(
            "REJECTED"
        )
        is False
    )


def test_pending_consensus_fails():

    assert (
        PolicyActivationEvaluation.evaluate(
            "PENDING"
        )
        is False
    )


def test_unknown_status_fails():

    assert (
        PolicyActivationEvaluation.evaluate(
            "UNKNOWN"
        )
        is False
    )
