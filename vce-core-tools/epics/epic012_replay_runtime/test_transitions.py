from epics.epic012_replay_runtime.transition_validator import (
    validate_transitions,
)


def test_accepts_valid_transition_sequence():

    valid_events = [
        {
            "lsn": 1,
            "opcode": "APPEND_EVIDENCE",
            "payload": "artifact-001",
        },
        {
            "lsn": 2,
            "opcode": "SEAL_SNAPSHOT",
            "payload": "snapshot-001",
        },
    ]

    assert (
        validate_transitions(valid_events)
        is True
    )


def test_rejects_invalid_transition_sequence():

    invalid_events = [
        {
            "lsn": 1,
            "opcode": "SEAL_SNAPSHOT",
            "payload": "snapshot-001",
        }
    ]

    assert (
        validate_transitions(invalid_events)
        is False
    )
