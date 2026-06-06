from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


def test_recovers_records_until_first_corruption():

    wal_lines = [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
        "INVALID|SEAL_SNAPSHOT|snapshot-001",
        "4|APPEND_EVIDENCE|artifact-002",
    ]

    recovery = WALRecovery()

    recovered = recovery.recover_until_corruption(
        wal_lines
    )

    assert recovered == [
        "1|APPEND_EVIDENCE|artifact-001",
        "2|REGISTER_ARTIFACT|artifact-001",
    ]
