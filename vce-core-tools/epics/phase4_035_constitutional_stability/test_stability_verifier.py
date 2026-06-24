from epics.phase4_035_constitutional_stability.stability_state import (
    StabilityState,
)
from epics.phase4_035_constitutional_stability.stability_verifier import (
    verify_stability_state,
)


def test_stability_verification_succeeds():
    state = StabilityState(100, 40, 60)

    result = verify_stability_state(state)

    assert result["verified"] is True


def test_stability_verification_fails():
    state = StabilityState(100, 140, -40)

    result = verify_stability_state(state)

    assert result["verified"] is False


def test_reports_net_stability():
    state = StabilityState(100, 25, 75)

    result = verify_stability_state(state)

    assert result["net_stability"] == 75
