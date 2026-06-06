from epics.epic012_replay_runtime.attestation import (
    ExecutionAttestation,
)
from epics.epic012_replay_runtime.runtime_core import (
    RuntimeCore,
)


def test_execution_attestation_contains_expected_fields():

    events = [
        {
            "lsn": 1,
            "opcode": "APPEND_EVIDENCE",
            "payload": "artifact-001",
        },
        {
            "lsn": 2,
            "opcode": "REGISTER_ARTIFACT",
            "payload": "artifact-001",
        },
        {
            "lsn": 3,
            "opcode": "SEAL_SNAPSHOT",
            "payload": "snapshot-001",
        },
    ]

    runtime = RuntimeCore()
    state = runtime.execute(events)

    builder = ExecutionAttestation()
    attestation = builder.build(
        events,
        state,
    )

    assert attestation["attestation_type"] == "VCE_RUNTIME_EXECUTION"
    assert attestation["sequence_number"] == 3
    assert attestation["state_hash"] == state.state_hash
    assert attestation["verified"] is True
