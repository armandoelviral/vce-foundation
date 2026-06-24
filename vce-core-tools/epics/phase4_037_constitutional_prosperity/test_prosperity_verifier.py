from epics.phase4_037_constitutional_prosperity.prosperity_state import ProsperityState
from epics.phase4_037_constitutional_prosperity.prosperity_verifier import (
    verify_prosperity_state,
)


def test_prosperity_verification_succeeds():
    state = ProsperityState(100, 40, 60)
    result = verify_prosperity_state(state)

    assert result["verified"] is True


def test_prosperity_verification_fails():
    state = ProsperityState(100, 140, -40)
    result = verify_prosperity_state(state)

    assert result["verified"] is False


def test_reports_net_prosperity():
    state = ProsperityState(100, 25, 75)
    result = verify_prosperity_state(state)

    assert result["net_prosperity"] == 75
