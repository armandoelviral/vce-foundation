from epics.ztc19_governance_ledger.governance_event import (
    GovernanceEvent,
)


def test_event_contains_event_id():

    event = GovernanceEvent(
        event_id="event-001",
        event_type="incident_declaration",
        payload_hash="hash-001",
    )

    assert event.event_id == "event-001"


def test_event_contains_type_and_payload_hash():

    event = GovernanceEvent(
        event_id="event-001",
        event_type="incident_declaration",
        payload_hash="hash-001",
    )

    assert event.event_type == "incident_declaration"
    assert event.payload_hash == "hash-001"


def test_event_serializes():

    event = GovernanceEvent(
        event_id="event-001",
        event_type="incident_declaration",
        payload_hash="hash-001",
    )

    assert event.to_dict() == {
        "event_id": "event-001",
        "event_type": "incident_declaration",
        "payload_hash": "hash-001",
    }
