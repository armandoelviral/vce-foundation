from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


def test_detects_truncated_wal_record():

    wal_lines = [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "3|SEAL_SNAPSHOT",
    ]

    recovery = WALRecovery()

    assert (
        recovery.detect_truncation(
            wal_lines
        )
        is True
    )
