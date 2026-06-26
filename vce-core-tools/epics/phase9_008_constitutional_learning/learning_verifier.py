from epics.phase9_008_constitutional_learning.learning_state import (
    LearningState,
)


def verify_learning(
    state: LearningState,
):
    return {
        "verified": state.total_learning > 0,
        "total_learning": state.total_learning,
    }
