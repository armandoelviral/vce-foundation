from epics.phase4_032_constitutional_reserves.reserve_state import (
    ReserveState,
)
from epics.phase4_032_constitutional_reserves.reserve_verifier import (
    verify_reserve_state,
)


def test_reserve_verification_succeeds():
    state = ReserveState(
        total_reserves=100,
        total_consumed=40,
        remaining_reserves=60,
    )

    result = verify_reserve_state(state)

    assert result["verified"] is True


def test_reserve_verification_fails():
    state = ReserveState(
        total_reserves=100,
        total_consumed=120,
        remaining_reserves=-20,
    )

    result = verify_reserve_state(state)

    assert result["verified"] is False


def test_reports_remaining_reserves():
    state = ReserveState(
        total_reserves=100,
        total_consumed=25,
        remaining_reserves=75,
    )

    result = verify_reserve_state(state)

    assert result["remaining_reserves"] == 75
