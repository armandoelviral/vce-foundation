from epics.phase6_002_constitutional_reputation.reputation_state import (
    ReputationState,
)


def verify_reputation(
    state: ReputationState,
):
    return {
        "verified": state.total_score > 0,
        "total_score": state.total_score,
        "total_records": state.total_records,
    }
