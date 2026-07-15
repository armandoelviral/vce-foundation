from has.runtime.knowledge_state import (
    KnowledgeState,
)

STATE_ORDER = {
    KnowledgeState.OBSERVATION: 0,
    KnowledgeState.HYPOTHESIS: 1,
    KnowledgeState.CANDIDATE_PRINCIPLE: 2,
    KnowledgeState.PRINCIPLE: 3,
}
