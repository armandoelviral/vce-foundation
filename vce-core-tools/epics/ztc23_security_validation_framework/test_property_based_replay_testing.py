from epics.ztc23_security_validation_framework.property_based_replay_testing import (
    PropertyBasedReplayTesting,
)


def test_accepts_valid_replay_state():

    state = {
        "previous_sequence": 1,
        "current_sequence": 2,
        "event_count": 5,
        "state_hash": "hash-001",
    }

    assert PropertyBasedReplayTesting.validate(
        state
    )


def test_rejects_sequence_rollback():

    state = {
        "previous_sequence": 2,
        "current_sequence": 1,
        "event_count": 5,
        "state_hash": "hash-001",
    }

    assert not PropertyBasedReplayTesting.validate(
        state
    )


def test_rejects_negative_event_count():

    state = {
        "previous_sequence": 1,
        "current_sequence": 2,
        "event_count": -1,
        "state_hash": "hash-001",
    }

    assert not PropertyBasedReplayTesting.validate(
        state
    )


def test_rejects_missing_state_hash():

    state = {
        "previous_sequence": 1,
        "current_sequence": 2,
        "event_count": 5,
        "state_hash": "",
    }

    assert not PropertyBasedReplayTesting.validate(
        state
    )
