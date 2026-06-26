from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)
from epics.phase9_008_constitutional_learning.learning_registry import (
    LearningRegistry,
)
from epics.phase9_008_constitutional_learning.learning_state import (
    LearningState,
)
from epics.phase9_008_constitutional_learning.learning_verifier import (
    verify_learning,
)


def test_end_to_end_learning_flow():
    registry = LearningRegistry()

    registry.add(
        LearningRecord(
            "learning.001",
            "outcome.001",
            "Improve replay policy",
        )
    )

    registry.add(
        LearningRecord(
            "learning.002",
            "outcome.002",
            "Strengthen evidence validation",
        )
    )

    state = LearningState.from_records(
        registry.records()
    )

    verification = verify_learning(state)

    assert verification["verified"] is True
    assert verification["total_learning"] == 2
