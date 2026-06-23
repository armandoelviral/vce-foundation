from epics.phase4_026_institutional_capital.institutional_capital_state import (
    InstitutionalCapitalState,
)
from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def test_builds_institutional_capital_state():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="compliance",
            capital_delta=10,
            reason="compliance verified",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.002",
            source_domain="governance",
            capital_delta=15,
            reason="governance verified",
        )
    )

    state = InstitutionalCapitalState.from_registry(
        registry,
        "institution.alpha",
    )

    assert state.institution_id == "institution.alpha"
    assert state.total_capital == 25
    assert state.record_count == 2


def test_unknown_institution_has_zero_state():
    registry = InstitutionalCapitalRegistry()

    state = InstitutionalCapitalState.from_registry(
        registry,
        "institution.unknown",
    )

    assert state.total_capital == 0
    assert state.record_count == 0


def test_state_is_immutable_snapshot():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.001",
            source_domain="reputation",
            capital_delta=5,
            reason="reputation verified",
        )
    )

    state = InstitutionalCapitalState.from_registry(
        registry,
        "institution.alpha",
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="evidence.002",
            source_domain="governance",
            capital_delta=10,
            reason="later event",
        )
    )

    assert state.total_capital == 5
    assert state.record_count == 1
