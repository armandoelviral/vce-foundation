from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


def test_detects_corrupted_record():

    record = (
        "INVALID|APPEND_EVIDENCE|artifact"
    )

    recovery = WALRecovery()

    assert (
        recovery.detect_corruption(
            record
        )
        is True
    )


def test_accepts_valid_record():

    record = (
        "1|APPEND_EVIDENCE|artifact"
    )

    recovery = WALRecovery()

    assert (
        recovery.detect_corruption(
            record
        )
        is False
    )
