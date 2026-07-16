from has.runtime.allowed_transitions import (
    ALLOWED_TRANSITIONS,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_allowed_transition_contract():

    assert (
        (
            KnowledgeState.OBSERVATION,
            KnowledgeState.HYPOTHESIS,
        )
        in ALLOWED_TRANSITIONS
    )

    assert (
        (
            KnowledgeState.HYPOTHESIS,
            KnowledgeState.CANDIDATE_PRINCIPLE,
        )
        in ALLOWED_TRANSITIONS
    )

    assert (
        (
            KnowledgeState.CANDIDATE_PRINCIPLE,
            KnowledgeState.PRINCIPLE,
        )
        in ALLOWED_TRANSITIONS
    )


def test_rejects_invalid_transition_contract():

    assert (
        (
            KnowledgeState.OBSERVATION,
            KnowledgeState.PRINCIPLE,
        )
        not in ALLOWED_TRANSITIONS
    )

    assert (
        (
            KnowledgeState.PRINCIPLE,
            KnowledgeState.OBSERVATION,
        )
        not in ALLOWED_TRANSITIONS
    )
