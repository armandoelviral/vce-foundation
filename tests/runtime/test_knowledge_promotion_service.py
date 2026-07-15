from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_promotion_service import (
    KnowledgePromotionService,
)
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)


def make_observation(
    evidence: int = 0,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
        evidence_count=evidence,
    )


def make_service() -> KnowledgePromotionService:
    return KnowledgePromotionService(
        policy=ObservationPromotionPolicy(),
        promoter=KnowledgePromoter(),
    )


def test_not_promoted_without_evidence() -> None:
    service = make_service()

    updated = service.promote_observation(
        make_observation(),
    )

    assert updated.state is KnowledgeState.OBSERVATION


def test_promoted_with_evidence() -> None:
    service = make_service()

    updated = service.promote_observation(
        make_observation(evidence=1),
    )

    assert updated.state is KnowledgeState.HYPOTHESIS
