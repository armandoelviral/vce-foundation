from epics.phase4_032_constitutional_reserves.reserve_state import (
    ReserveState,
)


def verify_reserve_state(
    state: ReserveState,
) -> dict:
    return {
        "verified": state.remaining_reserves >= 0,
        "total_reserves": state.total_reserves,
        "total_consumed": state.total_consumed,
        "remaining_reserves": state.remaining_reserves,
    }
