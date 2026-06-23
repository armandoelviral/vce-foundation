from epics.phase4_029_constitutional_credit.credit_capacity import (
    calculate_credit_capacity,
)
from epics.phase4_029_constitutional_credit.credit_default import (
    CreditDefaultRecord,
)
from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)
from epics.phase4_029_constitutional_credit.credit_registry import (
    CreditRegistry,
)
from epics.phase4_029_constitutional_credit.credit_state import (
    CreditState,
)
from epics.phase4_029_constitutional_credit.credit_verifier import (
    verify_credit_state,
)


def test_end_to_end_constitutional_credit_flow():
    capital = 100
    capacity = calculate_credit_capacity(capital)

    registry = CreditRegistry()

    registry.add(
        CreditRecord(
            credit_id="credit.001",
            borrower_id="institution.alpha",
            credit_amount=60,
            obligation_reference="obligation.future.001",
        )
    )

    registry.add(
        CreditRecord(
            credit_id="credit.002",
            borrower_id="institution.alpha",
            credit_amount=20,
            obligation_reference="obligation.future.002",
        )
    )

    default = CreditDefaultRecord(
        default_id="default.001",
        credit_id="credit.002",
        reason="future obligation not fulfilled",
    )

    assert default.credit_id == "credit.002"

    state = CreditState.from_credits(
        registry.records()
    )

    assert state.credit_count == 2
    assert state.total_credit == 80

    verification = verify_credit_state(
        state=state,
        credit_capacity=capacity,
    )

    assert verification["verified"] is True
    assert verification["remaining_credit_capacity"] == 20
