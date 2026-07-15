from has.runtime.evidence_accumulator import EvidenceAccumulator
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_promotion_service import (
    KnowledgePromotionService,
)
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)


class ObservationToHypothesisTransition:
    """Accumulates evidence and promotes an Observation to Hypothesis."""

    def __init__(self) -> None:
        self._accumulator = EvidenceAccumulator()
        self._promotion = KnowledgePromotionService(
            policy=ObservationPromotionPolicy(),
            promoter=KnowledgePromoter(),
        )

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        artifact_with_evidence = self._accumulator.record(artifact)

        return self._promotion.promote_observation(
            artifact_with_evidence,
        )
