from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)

EVALUATION_PROFILES = {

    KnowledgeState.HYPOTHESIS:
        EvaluationRequirements(
            minimum_evidence=1,
        ),

    KnowledgeState.CANDIDATE_PRINCIPLE:
        EvaluationRequirements(
            minimum_evidence=3,
            minimum_independent_validations=1,
            minimum_destruction_attempts=2,
        ),

    KnowledgeState.PRINCIPLE:
        EvaluationRequirements(
            minimum_evidence=5,
            minimum_independent_validations=3,
            minimum_destruction_attempts=5,
        ),
}
