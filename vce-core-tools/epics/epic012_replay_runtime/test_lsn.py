from lsn_validator import validate_lsn

valid_events = [
    {"lsn": 1, "opcode": "APPEND_EVIDENCE", "payload": "artifact-001"},
    {"lsn": 2, "opcode": "REGISTER_ARTIFACT", "payload": "artifact-001"},
    {"lsn": 3, "opcode": "SEAL_SNAPSHOT", "payload": "snapshot-001"},
]

invalid_events = [
    {"lsn": 1, "opcode": "APPEND_EVIDENCE", "payload": "artifact-001"},
    {"lsn": 3, "opcode": "SEAL_SNAPSHOT", "payload": "snapshot-001"},
]

print(validate_lsn(valid_events))
print(validate_lsn(invalid_events))
