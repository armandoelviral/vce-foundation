from phase2.runtime_state_recovery.runtime_state_model import (
    RuntimeState,
)

from phase2.runtime_state_recovery.state_transition_applier import (
    StateTransitionApplier,
)


def test_apply_single_event():

    state = RuntimeState()

    applier = StateTransitionApplier()

    new_state = applier.apply(
        state=state,
        event={
            "lsn": 1,
            "opcode": "EVENT_A",
        },
    )

    assert new_state.events_applied == 1
    assert new_state.last_lsn == 1


def test_apply_multiple_events():

    state = RuntimeState()

    applier = StateTransitionApplier()

    state = applier.apply(
        state,
        {
            "lsn": 1,
            "opcode": "EVENT_A",
        },
    )

    state = applier.apply(
        state,
        {
            "lsn": 2,
            "opcode": "EVENT_B",
        },
    )

    assert state.events_applied == 2
    assert state.last_lsn == 2


def test_state_hash_changes():

    state = RuntimeState()

    applier = StateTransitionApplier()

    new_state = applier.apply(
        state,
        {
            "lsn": 1,
            "opcode": "EVENT_A",
        },
    )

    assert (
        new_state.state_hash
        != "GENESIS"
    )
