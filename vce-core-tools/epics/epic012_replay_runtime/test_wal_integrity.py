from epics.epic012_replay_runtime.wal_integrity import (
    verify_wal,
)


def test_wal_integrity_returns_hashes():

    records = [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "3|SEAL_SNAPSHOT|snapshot-001",
    ]

    hashes = verify_wal(
        records
    )

    assert len(hashes) == 3


def test_wal_integrity_generates_unique_hashes():

    records = [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "3|SEAL_SNAPSHOT|snapshot-001",
    ]

    hashes = verify_wal(
        records
    )

    assert len(set(hashes)) == len(hashes)
