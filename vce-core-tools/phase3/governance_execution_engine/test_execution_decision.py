from phase3.governance_execution_engine.execution_decision import (
    ExecutionDecision,
)


def test_execute_action():

    decision = (
        ExecutionDecision.from_authorization(
            True
        )
    )

    assert (
        decision.status
        == "EXECUTE_ACTION"
    )


def test_reject_action():

    decision = (
        ExecutionDecision.from_authorization(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_ACTION"
    )


def test_decision_serializes():

    decision = (
        ExecutionDecision.from_authorization(
            True
        )
    )

    assert decision.to_dict() == {
        "status":
            "EXECUTE_ACTION"
    }
