from epics.epic041_runtime_state.runtime_state import RuntimeState
from epics.epic057_runtime_opcode.runtime_opcode import RuntimeOpcode
from epics.epic059_transition_validator.transition_validator import (
    TransitionValidator,
)


def test_validates_append_event_transition():

    before = RuntimeState(
        event_count=1,
        last_sequence=1,
    )

    after = RuntimeState(
        event_count=2,
        last_sequence=2,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    validator = TransitionValidator()

    assert validator.validate(
        before,
        after,
        opcode,
    ) is True


def test_rejects_event_count_jump():

    before = RuntimeState(
        event_count=1,
        last_sequence=1,
    )

    after = RuntimeState(
        event_count=3,
        last_sequence=2,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    validator = TransitionValidator()

    assert validator.validate(
        before,
        after,
        opcode,
    ) is False


def test_rejects_sequence_rollback():

    before = RuntimeState(
        event_count=2,
        last_sequence=2,
    )

    after = RuntimeState(
        event_count=3,
        last_sequence=1,
    )

    opcode = RuntimeOpcode(
        name="APPEND_EVENT",
        payload={},
    )

    validator = TransitionValidator()

    assert validator.validate(
        before,
        after,
        opcode,
    ) is False
