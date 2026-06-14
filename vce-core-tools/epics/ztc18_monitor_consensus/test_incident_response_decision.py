from epics.ztc18_monitor_consensus.incident_response_decision import (
    IncidentResponseDecision,
)


def test_decision_contains_incident_id():

    decision = IncidentResponseDecision(
        incident_id="incident-001",
        approved=True,
    )

    assert decision.incident_id == "incident-001"


def test_decision_contains_approval_status():

    decision = IncidentResponseDecision(
        incident_id="incident-001",
        approved=True,
    )

    assert decision.approved is True


def test_decision_serializes():

    decision = IncidentResponseDecision(
        incident_id="incident-001",
        approved=False,
    )

    assert decision.to_dict() == {
        "incident_id": "incident-001",
        "approved": False,
    }
