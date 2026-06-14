from epics.ztc18_monitor_consensus.incident_declaration import (
    IncidentDeclaration,
)


def test_declaration_contains_incident_id():

    declaration = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=True,
    )

    assert declaration.incident_id == "incident-001"


def test_declaration_contains_reason_and_status():

    declaration = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=True,
    )

    assert declaration.reason == "transparency_divergence"
    assert declaration.declared is True


def test_declaration_serializes():

    declaration = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=True,
    )

    assert declaration.to_dict() == {
        "incident_id": "incident-001",
        "reason": "transparency_divergence",
        "declared": True,
    }
