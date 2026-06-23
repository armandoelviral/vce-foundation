from epics.phase4_026_institutional_capital.institutional_capital_accrual import (
    calculate_institutional_capital,
)
from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def test_calculates_total_institutional_capital():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.compliance.001",
            source_domain="compliance",
            capital_delta=10,
            reason="compliance verified",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.governance.001",
            source_domain="governance",
            capital_delta=15,
            reason="valid governance behavior",
        )
    )

    assert calculate_institutional_capital(registry, "institution.alpha") == 25


def test_capital_is_isolated_per_institution():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="compliance",
            capital_delta=10,
            reason="alpha compliance",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.beta",
            evidence_id="evidence.001",
            source_domain="constitutional_behavior",
            capital_delta=20,
            reason="beta constitutional conduct",
        )
    )

    assert calculate_institutional_capital(registry, "institution.alpha") == 10
    assert calculate_institutional_capital(registry, "institution.beta") == 20


def test_unknown_institution_has_zero_capital():
    registry = InstitutionalCapitalRegistry()

    assert calculate_institutional_capital(registry, "institution.unknown") == 0


def test_negative_record_reduces_capital():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.good.001",
            source_domain="governance",
            capital_delta=20,
            reason="valid governance",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.bad.001",
            source_domain="compliance",
            capital_delta=-8,
            reason="verified compliance breach",
        )
    )

    assert calculate_institutional_capital(registry, "institution.alpha") == 12
