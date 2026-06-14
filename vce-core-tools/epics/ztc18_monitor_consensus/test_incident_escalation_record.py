from epics.ztc18_monitor_consensus.incident_escalation_record import (
    IncidentEscalationRecord,
)


def test_escalation_contains_incident_id():

    escalation = IncidentEscalationRecord(
        incident_id="incident-001",
        action="suspend_witness",
        target="witness-003",
    )

    assert escalation.incident_id == "incident-001"


def test_escalation_contains_action_and_target():

    escalation = IncidentEscalationRecord(
        incident_id="incident-001",
        action="suspend_witness",
        target="witness-003",
    )

    assert escalation.action == "suspend_witness"
    assert escalation.target == "witness-003"


def test_escalation_serializes():

    escalation = IncidentEscalationRecord(
        incident_id="incident-001",
        action="suspend_witness",
        target="witness-003",
    )

    assert escalation.to_dict() == {
        "incident_id": "incident-001",
        "action": "suspend_witness",
        "target": "witness-003",
    }
