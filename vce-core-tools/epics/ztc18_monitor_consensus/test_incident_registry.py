from epics.ztc18_monitor_consensus.incident_declaration import (
    IncidentDeclaration,
)

from epics.ztc18_monitor_consensus.incident_registry import (
    IncidentRegistry,
)


def test_registry_stores_incident():

    registry = IncidentRegistry()

    incident = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=True,
    )

    registry.add(incident)

    assert registry.count() == 1


def test_registry_returns_incident():

    registry = IncidentRegistry()

    incident = IncidentDeclaration(
        incident_id="incident-001",
        reason="transparency_divergence",
        declared=True,
    )

    registry.add(incident)

    incidents = registry.all()

    assert len(incidents) == 1
    assert incidents[0].incident_id == "incident-001"


def test_registry_starts_empty():

    registry = IncidentRegistry()

    assert registry.count() == 0
