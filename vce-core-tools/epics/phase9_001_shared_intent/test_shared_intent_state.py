from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)
from epics.phase9_001_shared_intent.shared_intent_state import (
    SharedIntentState,
)


def test_builds_shared_intent_state():
    records = [
        SharedIntentRecord(
            "intent.001",
            "Preserve evidence",
            5,
        ),
        SharedIntentRecord(
            "intent.002",
            "Protect historical context",
            8,
        ),
    ]

    state = SharedIntentState.from_records(records)

    assert state.total_intents == 2
    assert state.total_participants == 13


def test_empty_shared_intent_state():
    state = SharedIntentState.from_records([])

    assert state.total_intents == 0
    assert state.total_participants == 0
