from epics.phase9_008_constitutional_learning.learning_state import (
    LearningState,
)
from epics.phase9_008_constitutional_learning.learning_verifier import (
    verify_learning,
)


def test_verify_learning():
    state = LearningState(
        total_learning=2,
    )

    result = verify_learning(state)

    assert result["verified"] is True


def test_verify_empty_learning():
    state = LearningState(
        total_learning=0,
    )

    result = verify_learning(state)

    assert result["verified"] is False
