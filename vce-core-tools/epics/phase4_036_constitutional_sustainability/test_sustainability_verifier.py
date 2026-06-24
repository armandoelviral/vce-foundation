from epics.phase4_036_constitutional_sustainability.sustainability_state import (
    SustainabilityState,
)
from epics.phase4_036_constitutional_sustainability.sustainability_verifier import (
    verify_sustainability_state,
)


def test_sustainability_verification_succeeds():
    state = SustainabilityState(
        total_sustainability=100,
        total_depletion=40,
        net_sustainability=60,
    )

    result = verify_sustainability_state(state)

    assert result["verified"] is True


def test_sustainability_verification_fails():
    state = SustainabilityState(
        total_sustainability=100,
        total_depletion=140,
        net_sustainability=-40,
    )

    result = verify_sustainability_state(state)

    assert result["verified"] is False


def test_reports_net_sustainability():
    state = SustainabilityState(
        total_sustainability=100,
        total_depletion=25,
        net_sustainability=75,
    )

    result = verify_sustainability_state(state)

    assert result["net_sustainability"] == 75
