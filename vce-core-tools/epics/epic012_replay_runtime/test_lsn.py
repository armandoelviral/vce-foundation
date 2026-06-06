from epics.epic012_replay_runtime.lsn_validator import validate_lsn


def test_accepts_contiguous_lsn_sequence():

    valid_events = [
        {"lsn": 1, "opcode": "APPEND_EVIDENCE", "payload": "artifact-001"},
        {"lsn": 2, "opcode": "REGISTER_ARTIFACT", "payload": "artifact-001"},
        {"lsn": 3, "opcode": "SEAL_SNAPSHOT", "payload": "snapshot-001"},
    ]

    assert validate_lsn(valid_events) is True


def test_rejects_lsn_gap():

    invalid_events = [
        {"lsn": 1, "opcode": "APPEND_EVIDENCE", "payload": "artifact-001"},
        {"lsn": 3, "opcode": "SEAL_SNAPSHOT", "payload": "snapshot-001"},
    ]

    assert validate_lsn(invalid_events) is False
