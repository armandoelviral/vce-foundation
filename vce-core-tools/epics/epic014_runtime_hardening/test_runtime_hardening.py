from schema_firewall import SchemaFirewall


firewall = SchemaFirewall()


valid_events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact-001"
    }
]


invalid_events = [
    {
        "lsn": "1",
        "opcode": "APPEND_EVIDENCE"
    }
]


print(
    firewall.validate_stream(
        valid_events
    )
)

print(
    firewall.validate_stream(
        invalid_events
    )
)
