from hypothesis import given
from hypothesis import strategies as st

from epics.epic041_runtime_state.runtime_state import RuntimeState
from epics.epic057_runtime_opcode.runtime_opcode import RuntimeOpcode
from epics.epic059_transition_validator.transition_validator import (
    TransitionValidator,
)


@given(st.integers(min_value=0, max_value=100))
def test_append_event_increments_state(sequence):

    before = RuntimeState(
        event_count=sequence,
        last_sequence=sequence,
    )

    after = RuntimeState(
        event_count=sequence + 1,
        last_sequence=sequence + 1,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    validator = TransitionValidator()

    assert validator.validate(before, after, opcode) is True


@given(st.integers(min_value=1, max_value=100))
def test_sequence_rollback_is_always_rejected(sequence):

    before = RuntimeState(
        event_count=sequence,
        last_sequence=sequence,
    )

    after = RuntimeState(
        event_count=sequence,
        last_sequence=sequence - 1,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    validator = TransitionValidator()

    assert validator.validate(before, after, opcode) is False
