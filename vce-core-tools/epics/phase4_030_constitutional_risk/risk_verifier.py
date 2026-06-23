from epics.phase4_030_constitutional_risk.risk_state import (
    RiskState,
)


def verify_risk_state(
    state: RiskState,
) -> dict:
    return {
        "verified": state.remaining_exposure >= 0,
        "total_exposure": state.total_exposure,
        "total_impact": state.total_impact,
        "remaining_exposure": state.remaining_exposure,
    }
