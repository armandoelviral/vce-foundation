from persistent_wal import PersistentWAL


wal = PersistentWAL()


r1 = wal.append(
    1,
    "APPEND_EVIDENCE",
    "artifact-001"
)


r2 = wal.append(
    2,
    "REGISTER_ARTIFACT",
    "artifact-001"
)


print(r1)

print(r2)


print(
    r2["previous_hash"]
    ==
    r1["current_hash"]
)
