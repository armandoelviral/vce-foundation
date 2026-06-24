from epics.phase6_003_constitutional_credibility.credibility_state import (
    CredibilityState,
)


def verify_credibility(
    state: CredibilityState,
):
    return {
        "verified": state.total_score > 0,
        "total_score": state.total_score,
        "total_records": state.total_records,
    }
