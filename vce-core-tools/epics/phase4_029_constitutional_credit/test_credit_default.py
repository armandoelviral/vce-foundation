from epics.phase4_029_constitutional_credit.credit_default import (
    CreditDefaultRecord,
)


def test_credit_default_creation():
    record = CreditDefaultRecord(
        default_id="default.001",
        credit_id="credit.001",
        reason="obligation not fulfilled",
    )

    assert record.default_id == "default.001"
    assert record.credit_id == "credit.001"
    assert record.reason == "obligation not fulfilled"


def test_rejects_empty_default_id():
    try:
        CreditDefaultRecord(
            default_id="",
            credit_id="credit.001",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "default_id" in str(exc)


def test_rejects_empty_credit_id():
    try:
        CreditDefaultRecord(
            default_id="default.001",
            credit_id="",
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "credit_id" in str(exc)


def test_rejects_empty_reason():
    try:
        CreditDefaultRecord(
            default_id="default.001",
            credit_id="credit.001",
            reason="",
        )
        assert False
    except ValueError as exc:
        assert "reason" in str(exc)
