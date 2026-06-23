from epics.phase4_026_institutional_capital.institutional_capital_loss import (
    create_institutional_capital_loss,
)


def test_creates_institutional_capital_loss_record():
    loss = create_institutional_capital_loss(
        institution_id="institution.alpha",
        evidence_id="evidence.breach.001",
        source_domain="compliance",
        loss_amount=12,
        reason="verified compliance breach",
    )

    assert loss.institution_id == "institution.alpha"
    assert loss.evidence_id == "evidence.breach.001"
    assert loss.source_domain == "compliance"
    assert loss.capital_delta == -12
    assert loss.reason == "verified compliance breach"


def test_rejects_zero_loss_amount():
    try:
        create_institutional_capital_loss(
            institution_id="institution.alpha",
            evidence_id="evidence.breach.001",
            source_domain="governance",
            loss_amount=0,
            reason="invalid zero loss",
        )
        assert False
    except ValueError as exc:
        assert "loss_amount" in str(exc)


def test_rejects_negative_loss_amount():
    try:
        create_institutional_capital_loss(
            institution_id="institution.alpha",
            evidence_id="evidence.breach.001",
            source_domain="governance",
            loss_amount=-5,
            reason="invalid negative loss",
        )
        assert False
    except ValueError as exc:
        assert "loss_amount" in str(exc)
