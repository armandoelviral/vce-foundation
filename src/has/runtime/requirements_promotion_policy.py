from dataclasses import dataclass

from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)
from has.runtime.promotion_requirements import PromotionRequirements


@dataclass(frozen=True, slots=True)
class RequirementsPromotionPolicy(KnowledgeTransitionPolicy):
    """Evaluates promotion requirements for one source state."""

    source_state: KnowledgeState
    requirements: PromotionRequirements

    def can_promote(
        self,
        artifact: KnowledgeArtifact,
    ) -> bool:
        if artifact.state is not self.source_state:
            return False

        return (
            artifact.evidence_count
            >= self.requirements.minimum_evidence
            and artifact.independent_validations
            >= self.requirements.minimum_independent_validations
            and artifact.destruction_attempts
            >= self.requirements.minimum_destruction_attempts
        )
