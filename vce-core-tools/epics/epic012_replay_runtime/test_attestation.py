from runtime_core import RuntimeCore
from attestation import ExecutionAttestation


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
state = runtime.execute(events)

builder = ExecutionAttestation()
attestation = builder.build(events, state)

print(attestation["attestation_type"])
print(attestation["sequence_number"])
print(attestation["state_hash"])
print(attestation["verified"])
