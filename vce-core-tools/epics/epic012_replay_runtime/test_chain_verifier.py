from epics.epic012_replay_runtime.chain_verifier import (
    verify_chain,
)
from epics.epic012_replay_runtime.persistent_wal import (
    PersistentWAL,
)


def test_chain_verifier_accepts_valid_chain():

    wal = PersistentWAL()

    records = [
        wal.append(1, "APPEND_EVIDENCE", "artifact-001"),
        wal.append(2, "REGISTER_ARTIFACT", "artifact-001"),
        wal.append(3, "SEAL_SNAPSHOT", "snapshot-001"),
    ]

    assert verify_chain(records) is True


def test_chain_verifier_detects_tampering():

    wal = PersistentWAL()

    records = [
        wal.append(1, "APPEND_EVIDENCE", "artifact-001"),
        wal.append(2, "REGISTER_ARTIFACT", "artifact-001"),
        wal.append(3, "SEAL_SNAPSHOT", "snapshot-001"),
    ]

    records[0]["payload"] = "artifact-TAMPERED"

    assert verify_chain(records) is False
