from epics.phase4_029_constitutional_credit.credit_state import (
    CreditState,
)
from epics.phase4_029_constitutional_credit.credit_verifier import (
    verify_credit_state,
)


def test_credit_verification_succeeds_within_capacity():
    state = CreditState(
        credit_count=2,
        total_credit=80,
    )

    result = verify_credit_state(
        state=state,
        credit_capacity=100,
    )

    assert result["verified"] is True
    assert result["remaining_credit_capacity"] == 20


def test_credit_verification_fails_when_capacity_exceeded():
    state = CreditState(
        credit_count=3,
        total_credit=120,
    )

    result = verify_credit_state(
        state=state,
        credit_capacity=100,
    )

    assert result["verified"] is False
    assert result["remaining_credit_capacity"] == -20


def test_rejects_negative_credit_capacity():
    state = CreditState(
        credit_count=0,
        total_credit=0,
    )

    try:
        verify_credit_state(
            state=state,
            credit_capacity=-1,
        )
        assert False
    except ValueError as exc:
        assert "credit_capacity" in str(exc)
