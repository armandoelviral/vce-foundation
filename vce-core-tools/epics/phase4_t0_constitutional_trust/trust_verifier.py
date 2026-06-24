from epics.phase4_t0_constitutional_trust.trust_state import (
    TrustState,
)


def verify_trust_state(
    state: TrustState,
):
    return {
        "verified": state.net_trust >= 0,
        "total_trust": state.total_trust,
        "total_loss": state.total_loss,
        "net_trust": state.net_trust,
    }
