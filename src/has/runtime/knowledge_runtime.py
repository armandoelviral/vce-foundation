from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.runtime_result import RuntimeResult
from has.runtime.transitions.observation_to_hypothesis_transition import (
    ObservationToHypothesisTransition,
)


class KnowledgeRuntime:
    def __init__(self) -> None:
        self._observation_transition = (
            ObservationToHypothesisTransition()
        )

    def record_observation(
        self,
        artifact: KnowledgeArtifact,
    ) -> RuntimeResult:

        updated = (
            self._observation_transition.execute(
                artifact
            )
        )

        return RuntimeResult(
            artifact=updated,
            transition_executed=(
                updated != artifact
            ),
        )
