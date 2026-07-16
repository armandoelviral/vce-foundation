from has.runtime.evaluation_profiles import (
    EVALUATION_PROFILES,
)
from has.runtime.evidence_accumulator import (
    EvidenceAccumulator,
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
from has.runtime.transitions.evidence_recording_transition import (
    EvidenceRecordingTransition,
)
from has.runtime.transitions.knowledge_transition import (
    KnowledgeTransition,
)


class ObservationToHypothesisTransition(
    KnowledgeTransition,
):
    """Records evidence, evaluates readiness and advances to Hypothesis."""

    def __init__(self) -> None:

        self._evidence_transition = (
            EvidenceRecordingTransition(
                EvidenceAccumulator(),
            )
        )

        self._evaluator = (
            KnowledgeEvaluator()
        )

        self._requirements = (
            EVALUATION_PROFILES[
                KnowledgeState.HYPOTHESIS
            ]
        )

        self._state_transition = (
            StateTransition()
        )

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:

        if (
            artifact.state
            is not KnowledgeState.OBSERVATION
        ):
            return artifact

        artifact = (
            self._evidence_transition.execute(
                artifact,
            )
        )

        evaluation = (
            self._evaluator.evaluate(
                artifact,
                source_state=KnowledgeState.OBSERVATION,
                requirements=self._requirements,
            )
        )

        if not evaluation.eligible:
            return artifact

        return self._state_transition.apply(
            artifact,
            KnowledgeState.HYPOTHESIS,
        )
