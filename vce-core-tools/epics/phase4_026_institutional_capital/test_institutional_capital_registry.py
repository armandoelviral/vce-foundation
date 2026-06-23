from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def test_registry_stores_records_by_institution():
    registry = InstitutionalCapitalRegistry()

    record = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.001",
        source_domain="compliance",
        capital_delta=10,
        reason="compliance verified",
    )

    registry.add(record)

    records = registry.records_for("institution.alpha")

    assert records == [record]


def test_registry_returns_empty_for_unknown_institution():
    registry = InstitutionalCapitalRegistry()

    assert registry.records_for("institution.unknown") == []


def test_registry_rejects_duplicate_evidence_for_same_institution():
    registry = InstitutionalCapitalRegistry()

    first = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.001",
        source_domain="compliance",
        capital_delta=10,
        reason="first claim",
    )

    duplicate = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.001",
        source_domain="governance",
        capital_delta=5,
        reason="duplicate claim",
    )

    registry.add(first)

    try:
        registry.add(duplicate)
        assert False
    except ValueError as exc:
        assert "duplicate evidence" in str(exc)


def test_registry_all_records_are_append_only_copy():
    registry = InstitutionalCapitalRegistry()

    record = InstitutionalCapitalRecord(
        institution_id="institution.alpha",
        evidence_id="evidence.001",
        source_domain="reputation",
        capital_delta=7,
        reason="verified reputation conduct",
    )

    registry.add(record)

    records = registry.records_for("institution.alpha")
    records.clear()

    assert registry.records_for("institution.alpha") == [record]
