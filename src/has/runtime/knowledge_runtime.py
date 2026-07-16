from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.runtime_result import RuntimeResult
from has.runtime.transitions.candidate_principle_to_principle_transition import (
    CandidatePrincipleToPrincipleTransition,
)
from has.runtime.transitions.hypothesis_to_candidate_principle_transition import (
    HypothesisToCandidatePrincipleTransition,
)
from has.runtime.transitions.observation_to_hypothesis_transition import (
    ObservationToHypothesisTransition,
)


class KnowledgeRuntime:
    """Public facade for executable knowledge-state transitions."""

    def __init__(self) -> None:
        self._observation_to_hypothesis = (
            ObservationToHypothesisTransition()
        )
        self._hypothesis_to_candidate_principle = (
            HypothesisToCandidatePrincipleTransition()
        )
        self._candidate_principle_to_principle = (
            CandidatePrincipleToPrincipleTransition()
        )

    def record_observation(
        self,
        artifact: KnowledgeArtifact,
    ) -> RuntimeResult:
        updated = self._observation_to_hypothesis.execute(
            artifact,
        )

        return self._result(
            original=artifact,
            updated=updated,
        )

    def evaluate_hypothesis(
        self,
        artifact: KnowledgeArtifact,
    ) -> RuntimeResult:
        updated = self._hypothesis_to_candidate_principle.execute(
            artifact,
        )

        return self._result(
            original=artifact,
            updated=updated,
        )

    def evaluate_candidate_principle(
        self,
        artifact: KnowledgeArtifact,
    ) -> RuntimeResult:
        updated = self._candidate_principle_to_principle.execute(
            artifact,
        )

        return self._result(
            original=artifact,
            updated=updated,
        )

    @staticmethod
    def _result(
        *,
        original: KnowledgeArtifact,
        updated: KnowledgeArtifact,
    ) -> RuntimeResult:
        return RuntimeResult(
            artifact=updated,
            transition_executed=(
                updated.state is not original.state
            ),
        )
