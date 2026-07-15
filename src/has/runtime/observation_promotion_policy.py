from dataclasses import dataclass

from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)


@dataclass(frozen=True, slots=True)
class ObservationPromotionPolicy(KnowledgeTransitionPolicy):
    """Determines whether an Observation may advance to Hypothesis."""

    minimum_evidence: int = 1

    def __post_init__(self) -> None:
        if self.minimum_evidence < 1:
            raise ValueError("minimum_evidence must be at least 1")

    def can_promote(
        self,
        artifact: KnowledgeArtifact,
    ) -> bool:
        return (
            artifact.state is KnowledgeState.OBSERVATION
            and artifact.evidence_count >= self.minimum_evidence
        )
