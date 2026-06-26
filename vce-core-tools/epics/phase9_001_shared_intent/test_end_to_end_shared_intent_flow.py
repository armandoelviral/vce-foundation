from epics.phase9_001_shared_intent.shared_intent_record import (
    SharedIntentRecord,
)
from epics.phase9_001_shared_intent.shared_intent_registry import (
    SharedIntentRegistry,
)
from epics.phase9_001_shared_intent.shared_intent_state import (
    SharedIntentState,
)
from epics.phase9_001_shared_intent.shared_intent_verifier import (
    verify_shared_intent,
)


def test_end_to_end_shared_intent_flow():
    registry = SharedIntentRegistry()

    registry.add(
        SharedIntentRecord(
            "intent.001",
            "Preserve evidence",
            5,
        )
    )

    registry.add(
        SharedIntentRecord(
            "intent.002",
            "Protect historical context",
            8,
        )
    )

    state = SharedIntentState.from_records(
        registry.records()
    )

    verification = verify_shared_intent(state)

    assert verification["verified"] is True
    assert verification["total_participants"] == 13
