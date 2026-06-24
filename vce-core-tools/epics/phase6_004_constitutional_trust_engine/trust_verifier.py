from epics.phase6_004_constitutional_trust_engine.trust_state import (
    TrustState,
)


def verify_trust(
    state: TrustState,
):
    return {
        "verified": state.total_score > 0,
        "total_score": state.total_score,
        "total_records": state.total_records,
    }
