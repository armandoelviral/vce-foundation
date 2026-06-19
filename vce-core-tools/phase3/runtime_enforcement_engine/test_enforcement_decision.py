from phase3.runtime_enforcement_engine.enforcement_decision import (
    EnforcementDecision,
)


def test_execute_decision():

    decision = (
        EnforcementDecision.from_evaluation(
            "EXECUTE"
        )
    )

    assert (
        decision.status
        == "EXECUTE"
    )


def test_block_decision():

    decision = (
        EnforcementDecision.from_evaluation(
            "BLOCK"
        )
    )

    assert (
        decision.status
        == "BLOCK"
    )


def test_decision_serializes():

    decision = (
        EnforcementDecision.from_evaluation(
            "EXECUTE"
        )
    )

    assert decision.to_dict() == {
        "status": "EXECUTE"
    }
