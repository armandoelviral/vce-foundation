from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)


def test_credit_record_creation():
    record = CreditRecord(
        credit_id="credit.001",
        borrower_id="institution.alpha",
        credit_amount=100,
        obligation_reference="obligation.001",
    )

    assert record.credit_id == "credit.001"
    assert record.borrower_id == "institution.alpha"
    assert record.credit_amount == 100
    assert record.obligation_reference == "obligation.001"


def test_rejects_empty_credit_id():
    try:
        CreditRecord(
            credit_id="",
            borrower_id="institution.alpha",
            credit_amount=100,
            obligation_reference="obligation.001",
        )
        assert False
    except ValueError as exc:
        assert "credit_id" in str(exc)


def test_rejects_non_positive_credit_amount():
    try:
        CreditRecord(
            credit_id="credit.001",
            borrower_id="institution.alpha",
            credit_amount=0,
            obligation_reference="obligation.001",
        )
        assert False
    except ValueError as exc:
        assert "credit_amount" in str(exc)


def test_rejects_empty_obligation_reference():
    try:
        CreditRecord(
            credit_id="credit.001",
            borrower_id="institution.alpha",
            credit_amount=100,
            obligation_reference="",
        )
        assert False
    except ValueError as exc:
        assert "obligation_reference" in str(exc)
