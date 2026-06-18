from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)


def test_state_starts_empty():

    state = RuntimeState()

    assert state.events_applied == 0
    assert state.last_lsn == 0


def test_state_contains_hash():

    state = RuntimeState(
        events_applied=2,
        last_lsn=10,
        state_hash="hash-001",
    )

    assert state.state_hash == "hash-001"


def test_state_serializes():

    state = RuntimeState(
        events_applied=2,
        last_lsn=10,
        state_hash="hash-001",
    )

    assert state.to_dict() == {
        "events_applied": 2,
        "last_lsn": 10,
        "state_hash": "hash-001",
    }
