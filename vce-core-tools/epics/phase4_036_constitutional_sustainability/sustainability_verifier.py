from epics.phase4_036_constitutional_sustainability.sustainability_state import (
    SustainabilityState,
)


def verify_sustainability_state(state: SustainabilityState):
    return {
        "verified": state.net_sustainability >= 0,
        "total_sustainability": state.total_sustainability,
        "total_depletion": state.total_depletion,
        "net_sustainability": state.net_sustainability,
    }
