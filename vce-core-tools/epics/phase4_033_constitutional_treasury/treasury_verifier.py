from epics.phase4_033_constitutional_treasury.treasury_state import (
    TreasuryState,
)


def verify_treasury_state(
    state: TreasuryState,
):
    return {
        "verified": state.remaining_capacity >= 0,
        "total_allocated": state.total_allocated,
        "total_disbursed": state.total_disbursed,
        "remaining_capacity": state.remaining_capacity,
    }
