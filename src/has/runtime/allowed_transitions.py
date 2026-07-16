from has.runtime.knowledge_state import (
    KnowledgeState,
)

ALLOWED_TRANSITIONS = frozenset({
    (
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
    ),
    (
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
    ),
    (
        KnowledgeState.CANDIDATE_PRINCIPLE,
        KnowledgeState.PRINCIPLE,
    ),
})
