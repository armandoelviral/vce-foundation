from hypothesis import given
from hypothesis import strategies as st

from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


@given(
    st.integers(
        min_value=1,
        max_value=50,
    )
)
def test_recovery_returns_valid_prefix_before_corruption(length):

    valid_prefix = [
        f"{index}|APPEND_EVIDENCE|artifact-{index}"
        for index in range(1, length + 1)
    ]

    corrupted_tail = [
        "INVALID|SEAL_SNAPSHOT|snapshot",
        "999|APPEND_EVIDENCE|artifact-after-corruption",
    ]

    wal_lines = (
        valid_prefix
        + corrupted_tail
    )

    recovery = WALRecovery()

    recovered = recovery.recover_after_crash(
        wal_lines
    )

    assert recovered == valid_prefix
