from epics.phase9_008_constitutional_learning.learning_record import (
    LearningRecord,
)
from epics.phase9_008_constitutional_learning.learning_state import (
    LearningState,
)


def test_build_learning_state():
    records = [
        LearningRecord(
            "learning.001",
            "outcome.001",
            "Lesson A",
        ),
        LearningRecord(
            "learning.002",
            "outcome.002",
            "Lesson B",
        ),
    ]

    state = LearningState.from_records(records)

    assert state.total_learning == 2


def test_empty_learning_state():
    state = LearningState.from_records([])

    assert state.total_learning == 0
