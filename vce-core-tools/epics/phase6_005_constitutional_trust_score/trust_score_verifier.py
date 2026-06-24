from epics.phase6_005_constitutional_trust_score.trust_score_state import (
    TrustScoreState,
)


def verify_trust_score(
    state: TrustScoreState,
):
    return {
        "verified": state.average_score > 0,
        "average_score": state.average_score,
        "total_records": state.total_records,
    }
