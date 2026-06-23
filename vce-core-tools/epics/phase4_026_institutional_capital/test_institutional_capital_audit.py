from epics.phase4_026_institutional_capital.institutional_capital_audit import (
    audit_institutional_capital,
)
from epics.phase4_026_institutional_capital.institutional_capital_loss import (
    create_institutional_capital_loss,
)
from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def test_audit_returns_total_and_records():
    registry = InstitutionalCapitalRegistry()

    gain = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.good.001",
        source_domain="governance",
        capital_delta=20,
        reason="valid governance",
    )

    loss = create_institutional_capital_loss(
        institution_id="institution.alpha",
        evidence_id="evidence.bad.001",
        source_domain="compliance",
        loss_amount=5,
        reason="verified compliance breach",
    )

    registry.add(gain)
    registry.add(loss)

    audit = audit_institutional_capital(registry, "institution.alpha")

    assert audit["institution_id"] == "institution.alpha"
    assert audit["total_capital"] == 15
    assert audit["record_count"] == 2
    assert audit["records"] == [gain, loss]


def test_audit_separates_positive_and_negative_records():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.good.001",
            source_domain="constitutional_behavior",
            capital_delta=30,
            reason="constitutional conduct",
        )
    )

    registry.add(
        create_institutional_capital_loss(
            institution_id="institution.alpha",
            evidence_id="evidence.bad.001",
            source_domain="governance",
            loss_amount=10,
            reason="governance breach",
        )
    )

    audit = audit_institutional_capital(registry, "institution.alpha")

    assert audit["positive_capital"] == 30
    assert audit["negative_capital"] == -10
    assert audit["total_capital"] == 20


def test_audit_empty_institution():
    registry = InstitutionalCapitalRegistry()

    audit = audit_institutional_capital(registry, "institution.unknown")

    assert audit["institution_id"] == "institution.unknown"
    assert audit["total_capital"] == 0
    assert audit["positive_capital"] == 0
    assert audit["negative_capital"] == 0
    assert audit["record_count"] == 0
    assert audit["records"] == []
