from hypothesis import given
from hypothesis import strategies as st

from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


@given(
    st.lists(
        st.text(),
        min_size=0,
        max_size=100,
    )
)
def test_wal_recovery_never_crashes(wal_lines):

    recovery = WALRecovery()

    recovered = recovery.recover_after_crash(
        wal_lines
    )

    assert isinstance(
        recovered,
        list,
    )
