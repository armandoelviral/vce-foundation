from epics.phase9_004_constitutional_decision.decision_state import (
    DecisionState,
)


def verify_decisions(
    state: DecisionState,
):
    return {
        "verified": state.total_decisions > 0,
        "accepted": state.accepted,
        "rejected": state.rejected,
        "total_decisions": state.total_decisions,
    }
