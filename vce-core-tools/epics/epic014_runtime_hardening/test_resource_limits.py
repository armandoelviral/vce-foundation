from resource_limits import ResourceLimits


limits = ResourceLimits(
    max_events=2,
    max_payload_size=10
)


valid = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact"
    }
]


too_many = [
    {"payload": "x"},
    {"payload": "x"},
    {"payload": "x"}
]


too_large = [
    {
        "payload": "X" * 100
    }
]


print(
    limits.validate_stream(
        valid
    )
)


print(
    limits.validate_stream(
        too_many
    )
)


print(
    limits.validate_stream(
        too_large
    )
)
