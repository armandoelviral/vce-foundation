from epics.phase4_035_constitutional_stability.stability_state import (
    StabilityState,
)


def verify_stability_state(state: StabilityState):
    return {
        "verified": state.net_stability >= 0,
        "total_stability": state.total_stability,
        "total_loss": state.total_loss,
        "net_stability": state.net_stability,
    }
