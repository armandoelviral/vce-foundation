from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)


def create_institutional_capital_loss(
    institution_id: str,
    evidence_id: str,
    source_domain: str,
    loss_amount: int,
    reason: str,
) -> InstitutionalCapitalRecord:
    if loss_amount <= 0:
        raise ValueError("loss_amount must be greater than zero")

    return InstitutionalCapitalRecord(
        institution_id=institution_id,
        evidence_id=evidence_id,
        source_domain=source_domain,
        capital_delta=-loss_amount,
        reason=reason,
    )
