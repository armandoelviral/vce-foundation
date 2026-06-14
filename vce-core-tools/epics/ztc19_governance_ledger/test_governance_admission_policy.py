from epics.ztc19_governance_ledger.governance_event import (
    GovernanceEvent,
)

from epics.ztc19_governance_ledger.governance_admission_policy import (
    GovernanceAdmissionPolicy,
)


def test_accepts_known_event_type():

    policy = GovernanceAdmissionPolicy()

    event = GovernanceEvent(
        event_id="event-001",
        event_type="incident_declaration",
        payload_hash="hash-001",
    )

    assert policy.accept(event)


def test_rejects_unknown_event_type():

    policy = GovernanceAdmissionPolicy()

    event = GovernanceEvent(
        event_id="event-001",
        event_type="unknown_event",
        payload_hash="hash-001",
    )

    assert not policy.accept(event)


def test_accepts_key_rotation_event():

    policy = GovernanceAdmissionPolicy()

    event = GovernanceEvent(
        event_id="event-001",
        event_type="key_rotation",
        payload_hash="hash-001",
    )

    assert policy.accept(event)
