from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)
from epics.phase9_008_constitutional_learning.learning_registry import (
    LearningRegistry,
)


def test_registry_adds_learning():
    registry = LearningRegistry()

    registry.add(
        LearningRecord(
            "learning.001",
            "outcome.001",
            "Replay policy improved audit quality",
        )
    )

    assert len(registry.records()) == 1
