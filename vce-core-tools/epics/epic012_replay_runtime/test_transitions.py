from transition_validator import validate_transitions

valid_events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact-001"
    },
    {
        "lsn": 2,
        "opcode": "SEAL_SNAPSHOT",
        "payload": "snapshot-001"
    }
]

invalid_events = [
    {
        "lsn": 1,
        "opcode": "SEAL_SNAPSHOT",
        "payload": "snapshot-001"
    }
]

print(
    validate_transitions(
        valid_events
    )
)

print(
    validate_transitions(
        invalid_events
    )
)
