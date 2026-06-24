from epics.phase8_002_trust_expiration.expiration_state import (
    ExpirationState,
)


def verify_expiration(
    state: ExpirationState,
):
    return {
        "verified": state.total_remaining_days > 0,
        "total_remaining_days": state.total_remaining_days,
        "total_records": state.total_records,
    }
