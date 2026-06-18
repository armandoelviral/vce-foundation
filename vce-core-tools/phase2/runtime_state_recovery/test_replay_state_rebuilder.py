from phase2.runtime_state_recovery.replay_state_rebuilder import (
    ReplayStateRebuilder,
)


def test_rebuild_empty_events_returns_initial_state():

    rebuilder = ReplayStateRebuilder()

    state = rebuilder.rebuild(
        events=[],
    )

    assert state.events_applied == 0
    assert state.last_lsn == 0
    assert state.state_hash == "GENESIS"


def test_rebuild_applies_all_events():

    rebuilder = ReplayStateRebuilder()

    state = rebuilder.rebuild(
        events=[
            {
                "lsn": 1,
                "opcode": "EVENT_A",
            },
            {
                "lsn": 2,
                "opcode": "EVENT_B",
            },
        ],
    )

    assert state.events_applied == 2
    assert state.last_lsn == 2


def test_rebuild_produces_deterministic_hash():

    rebuilder = ReplayStateRebuilder()

    events = [
        {
            "lsn": 1,
            "opcode": "EVENT_A",
        },
        {
            "lsn": 2,
            "opcode": "EVENT_B",
        },
    ]

    state_a = rebuilder.rebuild(
        events=events,
    )

    state_b = rebuilder.rebuild(
        events=events,
    )

    assert (
        state_a.state_hash
        == state_b.state_hash
    )
