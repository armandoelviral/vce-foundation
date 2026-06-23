from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)


def test_institutional_capital_record_creation():
    record = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.compliance.001",
        source_domain="compliance",
        capital_delta=10,
        reason="verified regulatory compliance",
    )

    assert record.institution_id == "institution.alpha"
    assert record.evidence_id == "evidence.compliance.001"
    assert record.source_domain == "compliance"
    assert record.capital_delta == 10
    assert record.reason == "verified regulatory compliance"


def test_institutional_capital_record_rejects_empty_institution():
    try:
        InstitutionalCapitalRecord(
            institution_id="",
            evidence_id="evidence.001",
            source_domain="governance",
            capital_delta=5,
            reason="valid governance conduct",
        )
        assert False
    except ValueError as exc:
        assert "institution_id" in str(exc)


def test_institutional_capital_record_rejects_empty_evidence():
    try:
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="",
            source_domain="governance",
            capital_delta=5,
            reason="valid governance conduct",
        )
        assert False
    except ValueError as exc:
        assert "evidence_id" in str(exc)


def test_institutional_capital_record_rejects_unknown_domain():
    try:
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="marketing",
            capital_delta=5,
            reason="unsupported domain",
        )
        assert False
    except ValueError as exc:
        assert "source_domain" in str(exc)
