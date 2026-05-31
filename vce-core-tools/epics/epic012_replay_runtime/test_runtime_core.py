from runtime_core import RuntimeCore


events = [
    {
        "lsn": 1,
        "opcode": "APPEND_EVIDENCE",
        "payload": "artifact-001"
    },
    {
        "lsn": 2,
        "opcode": "REGISTER_ARTIFACT",
        "payload": "artifact-001"
    },
    {
        "lsn": 3,
        "opcode": "SEAL_SNAPSHOT",
        "payload": "snapshot-001"
    }
]

runtime = RuntimeCore()

state_a = runtime.execute(events)
state_b = runtime.execute(events)

print(state_a.sequence_number)
print(state_a.state_hash)
print(state_a.state_hash == state_b.state_hash)
