from opcode_policy import OpcodePolicy


policy = OpcodePolicy()


valid = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact"
    }
]


malicious = [
    {
        "lsn": 1,
        "opcode": "DELETE_LEDGER",
        "payload": "attack"
    }
]


print(
    policy.validate_stream(
        valid
    )
)


print(
    policy.validate_stream(
        malicious
    )
)
