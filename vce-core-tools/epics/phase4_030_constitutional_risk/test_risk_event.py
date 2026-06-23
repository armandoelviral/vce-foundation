from epics.phase4_030_constitutional_risk.risk_event import (
    RiskEventRecord,
)


def test_risk_event_creation():
    event = RiskEventRecord(
        event_id="event.001",
        risk_id="risk.001",
        impact_amount=40,
        reason="partial default realized",
    )

    assert event.event_id == "event.001"
    assert event.risk_id == "risk.001"
    assert event.impact_amount == 40
    assert event.reason == "partial default realized"


def test_rejects_empty_event_id():
    try:
        RiskEventRecord(
            event_id="",
            risk_id="risk.001",
            impact_amount=40,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "event_id" in str(exc)


def test_rejects_non_positive_impact_amount():
    try:
        RiskEventRecord(
            event_id="event.001",
            risk_id="risk.001",
            impact_amount=0,
            reason="invalid",
        )
        assert False
    except ValueError as exc:
        assert "impact_amount" in str(exc)
