from epics.phase9_001_shared_intent.shared_intent_state import (
    SharedIntentState,
)
from epics.phase9_001_shared_intent.shared_intent_verifier import (
    verify_shared_intent,
)


def test_shared_intent_verified():
    state = SharedIntentState(
        total_intents=2,
        total_participants=13,
    )

    result = verify_shared_intent(state)

    assert result["verified"] is True


def test_empty_shared_intent_not_verified():
    state = SharedIntentState(
        total_intents=0,
        total_participants=0,
    )

    result = verify_shared_intent(state)

    assert result["verified"] is False
