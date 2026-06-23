from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)
from epics.phase4_026_institutional_capital.institutional_capital_verifier import (
    verify_institutional_capital,
)


def test_verifies_institution_above_required_capital():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="compliance",
            capital_delta=20,
            reason="compliance verified",
        )
    )

    result = verify_institutional_capital(
        registry=registry,
        institution_id="institution.alpha",
        required_capital=10,
    )

    assert result["verified"] is True
    assert result["institution_id"] == "institution.alpha"
    assert result["total_capital"] == 20
    assert result["required_capital"] == 10


def test_rejects_institution_below_required_capital():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="governance",
            capital_delta=5,
            reason="governance verified",
        )
    )

    result = verify_institutional_capital(
        registry=registry,
        institution_id="institution.alpha",
        required_capital=10,
    )

    assert result["verified"] is False
    assert result["total_capital"] == 5
    assert result["required_capital"] == 10


def test_unknown_institution_fails_verification():
    registry = InstitutionalCapitalRegistry()

    result = verify_institutional_capital(
        registry=registry,
        institution_id="institution.unknown",
        required_capital=1,
    )

    assert result["verified"] is False
    assert result["total_capital"] == 0


def test_rejects_negative_required_capital():
    registry = InstitutionalCapitalRegistry()

    try:
        verify_institutional_capital(
            registry=registry,
            institution_id="institution.alpha",
            required_capital=-1,
        )
        assert False
    except ValueError as exc:
        assert "required_capital" in str(exc)
