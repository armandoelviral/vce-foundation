from has.runtime.knowledge_state import (
    KnowledgeState,
)

from has.runtime.transition_validator import (
    TransitionValidator,
)


def test_forward_transition():

    validator = TransitionValidator()

    assert validator.can_transition(
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
    )


def test_same_state_is_invalid():

    validator = TransitionValidator()

    assert not validator.can_transition(
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.HYPOTHESIS,
    )


def test_backward_transition_is_invalid():

    validator = TransitionValidator()

    assert not validator.can_transition(
        KnowledgeState.PRINCIPLE,
        KnowledgeState.OBSERVATION,
    )
