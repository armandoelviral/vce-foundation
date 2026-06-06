from hypothesis import given
from hypothesis import strategies as st

from epics.epic012_replay_runtime.lsn_validator import (
    validate_lsn,
)


@given(
    st.integers(
        min_value=1,
        max_value=50,
    )
)
def test_contiguous_lsn_sequences_are_valid(length):

    events = [
        {
            "lsn": index,
            "opcode": "APPEND_EVIDENCE",
            "payload": "artifact",
        }
        for index in range(1, length + 1)
    ]

    assert validate_lsn(events) is True


@given(
    st.integers(
        min_value=3,
        max_value=50,
    )
)
def test_lsn_gap_is_rejected(length):

    events = [
        {
            "lsn": index,
            "opcode": "APPEND_EVIDENCE",
            "payload": "artifact",
        }
        for index in range(1, length + 1)
    ]

    events.pop(1)

    assert validate_lsn(events) is False
