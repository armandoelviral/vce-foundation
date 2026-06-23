from epics.phase4_026_institutional_capital.institutional_capital_loss import (
    create_institutional_capital_loss,
)
from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)
from epics.phase4_026_institutional_capital.institutional_capital_state import (
    InstitutionalCapitalState,
)
from epics.phase4_026_institutional_capital.institutional_capital_verifier import (
    verify_institutional_capital,
)


def test_end_to_end_institutional_capital_flow():
    registry = InstitutionalCapitalRegistry()

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="compliance.001",
            source_domain="compliance",
            capital_delta=20,
            reason="regulatory compliance verified",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="governance.001",
            source_domain="governance",
            capital_delta=15,
            reason="governance review passed",
        )
    )

    registry.add(
        InstitutionalCapitalRecord(
            institution_id="institution.alpha",
            evidence_id="constitutional.001",
            source_domain="constitutional_behavior",
            capital_delta=10,
            reason="constitutional behavior verified",
        )
    )

    registry.add(
        create_institutional_capital_loss(
            institution_id="institution.alpha",
            evidence_id="incident.001",
            source_domain="compliance",
            loss_amount=5,
            reason="minor compliance violation",
        )
    )

    state = InstitutionalCapitalState.from_registry(
        registry,
        "institution.alpha",
    )

    assert state.total_capital == 40
    assert state.record_count == 4

    verification = verify_institutional_capital(
        registry=registry,
        institution_id="institution.alpha",
        required_capital=30,
    )

    assert verification["verified"] is True
    assert verification["total_capital"] == 40
    assert verification["required_capital"] == 30
