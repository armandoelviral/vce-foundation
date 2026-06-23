from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)
from epics.phase4_029_constitutional_credit.credit_registry import (
    CreditRegistry,
)


def test_registry_stores_credit():
    registry = CreditRegistry()

    credit = CreditRecord(
        credit_id="credit.001",
        borrower_id="institution.alpha",
        credit_amount=100,
        obligation_reference="obligation.001",
    )

    registry.add(credit)

    assert registry.records() == [credit]


def test_registry_rejects_duplicate_credit():
    registry = CreditRegistry()

    credit = CreditRecord(
        credit_id="credit.001",
        borrower_id="institution.alpha",
        credit_amount=100,
        obligation_reference="obligation.001",
    )

    registry.add(credit)

    try:
        registry.add(credit)
        assert False
    except ValueError as exc:
        assert "duplicate credit" in str(exc)


def test_registry_returns_copy():
    registry = CreditRegistry()

    credit = CreditRecord(
        credit_id="credit.001",
        borrower_id="institution.alpha",
        credit_amount=100,
        obligation_reference="obligation.001",
    )

    registry.add(credit)

    records = registry.records()
    records.clear()

    assert len(registry.records()) == 1
