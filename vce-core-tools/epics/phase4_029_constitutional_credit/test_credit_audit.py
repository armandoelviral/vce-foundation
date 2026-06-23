from epics.phase4_029_constitutional_credit.credit_audit import (
    audit_credit_system,
)
from epics.phase4_029_constitutional_credit.credit_default import (
    CreditDefaultRecord,
)
from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)


def test_credit_audit_counts_credit_and_defaults():
    credits = [
        CreditRecord(
            credit_id="credit.001",
            borrower_id="institution.alpha",
            credit_amount=100,
            obligation_reference="obligation.001",
        ),
        CreditRecord(
            credit_id="credit.002",
            borrower_id="institution.beta",
            credit_amount=50,
            obligation_reference="obligation.002",
        ),
    ]

    defaults = [
        CreditDefaultRecord(
            default_id="default.001",
            credit_id="credit.001",
            reason="failed obligation",
        )
    ]

    audit = audit_credit_system(
        credits=credits,
        defaults=defaults,
    )

    assert audit["credit_count"] == 2
    assert audit["default_count"] == 1
    assert audit["total_credit"] == 150


def test_empty_audit():
    audit = audit_credit_system(
        credits=[],
        defaults=[],
    )

    assert audit["credit_count"] == 0
    assert audit["default_count"] == 0
    assert audit["total_credit"] == 0
