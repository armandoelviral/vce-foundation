from epics.phase9_004_constitutional_decision.decision_state import (
    DecisionState,
)
from epics.phase9_004_constitutional_decision.decision_verifier import (
    verify_decisions,
)


def test_verify_decisions():
    state = DecisionState(
        total_decisions=2,
        accepted=1,
        rejected=1,
    )

    result = verify_decisions(state)

    assert result["verified"] is True


def test_empty_decisions():
    state = DecisionState(
        total_decisions=0,
        accepted=0,
        rejected=0,
    )

    result = verify_decisions(state)

    assert result["verified"] is False
