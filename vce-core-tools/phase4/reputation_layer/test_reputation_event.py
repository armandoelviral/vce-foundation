from phase4.reputation_layer.reputation_event import (
    ReputationEvent,
)


def test_contains_did():

    event = ReputationEvent(
        citizen_did="did:tcn:test:01",
        event_type="response_valid",
        impact=10,
    )

    assert event.citizen_did == (
        "did:tcn:test:01"
    )


def test_contains_event_type():

    event = ReputationEvent(
        citizen_did="did:tcn:test:01",
        event_type="response_valid",
        impact=10,
    )

    assert event.event_type == (
        "response_valid"
    )


def test_contains_impact():

    event = ReputationEvent(
        citizen_did="did:tcn:test:01",
        event_type="response_valid",
        impact=10,
    )

    assert event.impact == 10


def test_serializes():

    event = ReputationEvent(
        citizen_did="did:tcn:test:01",
        event_type="response_valid",
        impact=10,
    )

    assert event.to_dict() == {
        "citizen_did": "did:tcn:test:01",
        "event_type": "response_valid",
        "impact": 10,
    }
