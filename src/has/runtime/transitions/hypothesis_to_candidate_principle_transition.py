from has.runtime.evaluation_profiles import (
    EVALUATION_PROFILES,
)
from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_evaluator import (
    KnowledgeEvaluator,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.state_transition import (
    StateTransition,
)
from has.runtime.transitions.knowledge_transition import (
    KnowledgeTransition,
)


class HypothesisToCandidatePrincipleTransition(
    KnowledgeTransition,
):
    """Evaluates and advances a Hypothesis to Candidate Principle."""

    def __init__(
        self,
        *,
        evaluator: KnowledgeEvaluator | None = None,
        state_transition: StateTransition | None = None,
        requirements: EvaluationRequirements | None = None,
    ) -> None:

        self._evaluator = (
            evaluator
            or KnowledgeEvaluator()
        )

        self._state_transition = (
            state_transition
            or StateTransition()
        )

        self._requirements = (
            requirements
            or EVALUATION_PROFILES[
                KnowledgeState.CANDIDATE_PRINCIPLE
            ]
        )

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:

        evaluation = (
            self._evaluator.evaluate(
                artifact,
                source_state=KnowledgeState.HYPOTHESIS,
                requirements=self._requirements,
            )
        )

        if not evaluation.eligible:
            return artifact

        return self._state_transition.apply(
            artifact,
            KnowledgeState.CANDIDATE_PRINCIPLE,
        )
