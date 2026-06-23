from epics.phase4_029_constitutional_credit.credit_record import (
    CreditRecord,
)
from epics.phase4_029_constitutional_credit.credit_default import (
    CreditDefaultRecord,
)


def audit_credit_system(
    credits: list[CreditRecord],
    defaults: list[CreditDefaultRecord],
) -> dict:
    return {
        "credit_count": len(credits),
        "default_count": len(defaults),
        "total_credit": sum(
            credit.credit_amount
            for credit in credits
        ),
    }
