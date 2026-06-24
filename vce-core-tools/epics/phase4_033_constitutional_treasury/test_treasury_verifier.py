from epics.phase4_033_constitutional_treasury.treasury_state import (
    TreasuryState,
)
from epics.phase4_033_constitutional_treasury.treasury_verifier import (
    verify_treasury_state,
)


def test_treasury_verification_succeeds():
    state = TreasuryState(
        total_allocated=100,
        total_disbursed=40,
        remaining_capacity=60,
    )

    result = verify_treasury_state(state)

    assert result["verified"] is True


def test_treasury_verification_fails():
    state = TreasuryState(
        total_allocated=100,
        total_disbursed=140,
        remaining_capacity=-40,
    )

    result = verify_treasury_state(state)

    assert result["verified"] is False


def test_reports_remaining_capacity():
    state = TreasuryState(
        total_allocated=100,
        total_disbursed=20,
        remaining_capacity=80,
    )

    result = verify_treasury_state(state)

    assert result["remaining_capacity"] == 80
