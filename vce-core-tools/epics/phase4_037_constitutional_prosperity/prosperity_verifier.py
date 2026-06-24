from epics.phase4_037_constitutional_prosperity.prosperity_state import ProsperityState


def verify_prosperity_state(state: ProsperityState):
    return {
        "verified": state.net_prosperity >= 0,
        "total_prosperity": state.total_prosperity,
        "total_loss": state.total_loss,
        "net_prosperity": state.net_prosperity,
    }
