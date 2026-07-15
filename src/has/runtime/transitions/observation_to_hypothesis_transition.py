from has.runtime.evidence_accumulator import EvidenceAccumulator
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)
from has.runtime.transitions.evidence_recording_transition import (
    EvidenceRecordingTransition,
)
from has.runtime.transitions.knowledge_transition import KnowledgeTransition
from has.runtime.transitions.promotion_transition import (
    PromotionTransition,
)


class ObservationToHypothesisTransition(KnowledgeTransition):
    """Coordinates evidence recording and Observation promotion."""

    def __init__(self) -> None:
        self._evidence_transition = EvidenceRecordingTransition(
            EvidenceAccumulator(),
        )
        self._promotion_transition = PromotionTransition(
            policy=ObservationPromotionPolicy(),
            promoter=KnowledgePromoter(),
            target_state=KnowledgeState.HYPOTHESIS,
        )

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        if artifact.state is not KnowledgeState.OBSERVATION:
            return artifact

        artifact_with_evidence = self._evidence_transition.execute(
            artifact,
        )

        return self._promotion_transition.execute(
            artifact_with_evidence,
        )
