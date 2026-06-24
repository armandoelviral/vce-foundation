from epics.phase8_001_temporal_validity.validity_state import (
    ValidityState,
)


def verify_validity(
    state: ValidityState,
):
    return {
        "verified": state.total_days > 0,
        "total_days": state.total_days,
        "total_records": state.total_records,
    }
