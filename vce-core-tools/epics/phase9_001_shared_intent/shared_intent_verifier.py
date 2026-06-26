from epics.phase9_001_shared_intent.shared_intent_state import (
    SharedIntentState,
)


def verify_shared_intent(
    state: SharedIntentState,
):
    return {
        "verified": (
            state.total_intents > 0
            and state.total_participants > 0
        ),
        "total_intents": state.total_intents,
        "total_participants": state.total_participants,
    }
