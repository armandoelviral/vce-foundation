from has.runtime.evaluation_profiles import EVALUATION_PROFILES
from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_evaluator import KnowledgeEvaluator
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.state_transition import StateTransition
from has.runtime.transitions.knowledge_transition import (
    KnowledgeTransition,
)


class CandidatePrincipleToPrincipleTransition(
    KnowledgeTransition,
):
    """Evaluates and advances a Candidate Principle to Principle."""

    def __init__(
        self,
        *,
        evaluator: KnowledgeEvaluator | None = None,
        state_transition: StateTransition | None = None,
        requirements: EvaluationRequirements | None = None,
    ) -> None:
        self._evaluator = evaluator or KnowledgeEvaluator()
        self._state_transition = (
            state_transition or StateTransition()
        )
        self._requirements = (
            requirements
            or EVALUATION_PROFILES[
                KnowledgeState.PRINCIPLE
            ]
        )

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        evaluation = self._evaluator.evaluate(
            artifact,
            source_state=KnowledgeState.CANDIDATE_PRINCIPLE,
            requirements=self._requirements,
        )

        if not evaluation.eligible:
            return artifact

        return self._state_transition.apply(
            artifact,
            KnowledgeState.PRINCIPLE,
        )
