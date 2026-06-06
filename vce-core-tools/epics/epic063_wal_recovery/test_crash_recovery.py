from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


def test_recovers_after_crash_with_corrupted_tail():

    wal_lines = [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "3|SEAL_SNAPSHOT|snapshot-001",
        "4|APPEND_EVIDENCE|",
        "5|REGISTER_ARTIFACT|artifact-002",
    ]

    recovery = WALRecovery()

    recovered = recovery.recover_after_crash(
        wal_lines
    )

    assert recovered == [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "3|SEAL_SNAPSHOT|snapshot-001",
    ]
