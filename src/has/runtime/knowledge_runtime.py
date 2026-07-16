from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.runtime_event import RuntimeEvent
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
        *,
        event_id: str,
    ) -> RuntimeResult:
        updated = self._observation_to_hypothesis.execute(
            artifact,
        )

        return self._result(
            event_id=event_id,
            original=artifact,
            updated=updated,
        )

    def evaluate_hypothesis(
        self,
        artifact: KnowledgeArtifact,
        *,
        event_id: str,
    ) -> RuntimeResult:
        updated = self._hypothesis_to_candidate_principle.execute(
            artifact,
        )

        return self._result(
            event_id=event_id,
            original=artifact,
            updated=updated,
        )

    def evaluate_candidate_principle(
        self,
        artifact: KnowledgeArtifact,
        *,
        event_id: str,
    ) -> RuntimeResult:
        updated = self._candidate_principle_to_principle.execute(
            artifact,
        )

        return self._result(
            event_id=event_id,
            original=artifact,
            updated=updated,
        )

    @staticmethod
    def _result(
        *,
        event_id: str,
        original: KnowledgeArtifact,
        updated: KnowledgeArtifact,
    ) -> RuntimeResult:
        transition_executed = (
            updated.state is not original.state
        )

        event = None

        if transition_executed:
            event = RuntimeEvent(
                event_id=event_id,
                artifact_id=original.identifier,
                from_state=original.state,
                to_state=updated.state,
                evaluation=EvaluationResult(
                    eligible=True,
                ),
            )

        return RuntimeResult(
            artifact=updated,
            transition_executed=transition_executed,
            event=event,
        )
