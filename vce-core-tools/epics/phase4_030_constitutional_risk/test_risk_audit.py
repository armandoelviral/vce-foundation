from epics.phase4_030_constitutional_risk.risk_audit import (
    audit_risk_system,
)
from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)
from epics.phase4_030_constitutional_risk.risk_record import (
    RiskRecord,
)


def test_risk_audit_counts_exposure_and_events():
    risks = [
        RiskRecord(
            risk_id="risk.001",
            actor_id="institution.alpha",
            exposure_amount=100,
            source_reference="credit.001",
            reason="credit exposure",
        ),
        RiskRecord(
            risk_id="risk.002",
            actor_id="institution.alpha",
            exposure_amount=50,
            source_reference="credit.002",
            reason="credit exposure",
        ),
    ]

    events = [
        RiskEventRecord(
            event_id="event.001",
            risk_id="risk.001",
            impact_amount=40,
            reason="partial default realized",
        )
    ]

    audit = audit_risk_system(risks=risks, events=events)

    assert audit["risk_count"] == 2
    assert audit["event_count"] == 1
    assert audit["total_exposure"] == 150
    assert audit["total_impact"] == 40


def test_empty_risk_audit():
    audit = audit_risk_system(risks=[], events=[])

    assert audit["risk_count"] == 0
    assert audit["event_count"] == 0
    assert audit["total_exposure"] == 0
    assert audit["total_impact"] == 0
