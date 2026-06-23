from epics.phase4_029_constitutional_credit.credit_state import (
    CreditState,
)


def verify_credit_state(
    state: CreditState,
    credit_capacity: int,
) -> dict:
    if credit_capacity < 0:
        raise ValueError("credit_capacity cannot be negative")

    remaining_credit_capacity = credit_capacity - state.total_credit

    return {
        "verified": remaining_credit_capacity >= 0,
        "credit_count": state.credit_count,
        "total_credit": state.total_credit,
        "credit_capacity": credit_capacity,
        "remaining_credit_capacity": remaining_credit_capacity,
    }
