from epics.epic012_replay_runtime.persistent_wal import PersistentWAL


def test_persistent_wal_links_entries_with_hash_chain():

    wal = PersistentWAL()

    r1 = wal.append(
        1,
        "APPEND_EVIDENCE",
        "artifact-001",
    )

    r2 = wal.append(
        2,
        "REGISTER_ARTIFACT",
        "artifact-001",
    )

    assert (
        r2["previous_hash"]
        == r1["current_hash"]
    )


def test_persistent_wal_records_lsn_opcode_and_payload():

    wal = PersistentWAL()

    record = wal.append(
        1,
        "APPEND_EVIDENCE",
        "artifact-001",
    )

    assert record["lsn"] == 1
    assert record["opcode"] == "APPEND_EVIDENCE"
    assert record["payload"] == "artifact-001"
