from persistent_wal import PersistentWAL
from chain_verifier import verify_chain


wal = PersistentWAL()

records = [
    wal.append(1, "APPEND_EVIDENCE", "artifact-001"),
    wal.append(2, "REGISTER_ARTIFACT", "artifact-001"),
    wal.append(3, "SEAL_SNAPSHOT", "snapshot-001"),
]

print(
    verify_chain(records)
)

records[0]["payload"] = "artifact-TAMPERED"

print(
    verify_chain(records)
)
