from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
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
    ) -> KnowledgeArtifact:

        return (
            self._observation_transition.execute(
                artifact
            )
        )
