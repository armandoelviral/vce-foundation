from epics.phase4_030_constitutional_risk.risk_state import (
    RiskState,
)
from epics.phase4_030_constitutional_risk.risk_verifier import (
    verify_risk_state,
)


def test_risk_verification_succeeds():
    state = RiskState(
        total_exposure=100,
        total_impact=40,
        remaining_exposure=60,
    )

    result = verify_risk_state(state)

    assert result["verified"] is True


def test_risk_verification_fails():
    state = RiskState(
        total_exposure=100,
        total_impact=150,
        remaining_exposure=-50,
    )

    result = verify_risk_state(state)

    assert result["verified"] is False


def test_reports_remaining_exposure():
    state = RiskState(
        total_exposure=100,
        total_impact=25,
        remaining_exposure=75,
    )

    result = verify_risk_state(state)

    assert result["remaining_exposure"] == 75
