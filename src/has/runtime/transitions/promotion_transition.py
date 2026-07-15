from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)
from has.runtime.transitions.knowledge_transition import KnowledgeTransition


class PromotionTransition(KnowledgeTransition):
    """Promotes an artifact when its policy permits the transition."""

    def __init__(
        self,
        *,
        policy: KnowledgeTransitionPolicy,
        promoter: KnowledgePromoter,
        target_state: KnowledgeState,
    ) -> None:
        self._policy = policy
        self._promoter = promoter
        self._target_state = target_state

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        if not self._policy.can_promote(artifact):
            return artifact

        return self._promoter.promote(
            artifact,
            self._target_state,
        )
