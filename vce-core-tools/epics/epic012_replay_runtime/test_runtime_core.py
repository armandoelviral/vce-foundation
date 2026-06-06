from epics.epic012_replay_runtime.runtime_core import RuntimeCore


def test_runtime_core_executes_deterministically():

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

    state_a = runtime.execute(events)
    state_b = runtime.execute(events)

    assert state_a.state_hash == state_b.state_hash
    assert state_a.sequence_number == 3
