from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)
from epics.phase4_029_constitutional_credit.credit_state import (
    CreditState,
)


def test_builds_credit_state():
    credits = [
        CreditRecord(
            credit_id="credit.001",
            borrower_id="institution.alpha",
            credit_amount=100,
            obligation_reference="obligation.001",
        ),
        CreditRecord(
            credit_id="credit.002",
            borrower_id="institution.alpha",
            credit_amount=50,
            obligation_reference="obligation.002",
        ),
    ]

    state = CreditState.from_credits(credits)

    assert state.credit_count == 2
    assert state.total_credit == 150


def test_empty_credit_state():
    state = CreditState.from_credits([])

    assert state.credit_count == 0
    assert state.total_credit == 0
