from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_promoter import (
    KnowledgePromoter,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)


class KnowledgePromotionService:

    def __init__(
        self,
        policy: ObservationPromotionPolicy,
        promoter: KnowledgePromoter,
    ) -> None:

        self._policy = policy
        self._promoter = promoter

    def promote_observation(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:

        if not self._policy.can_promote(
            artifact
        ):
            return artifact

        return self._promoter.promote(
            artifact,
            KnowledgeState.HYPOTHESIS,
        )
