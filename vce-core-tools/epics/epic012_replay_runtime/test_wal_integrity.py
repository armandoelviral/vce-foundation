from wal_integrity import verify_wal

records = [
    "1|APPEND_EVIDENCE|artifact-001",
    "2|REGISTER_ARTIFACT|artifact-001",
    "3|SEAL_SNAPSHOT|snapshot-001"
]

hashes = verify_wal(records)

for h in hashes:
    print(h)
