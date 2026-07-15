from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_promotion_service import (
    KnowledgePromotionService,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def make_observation(
    evidence=0,
):

    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
        evidence_count=evidence,
    )


def test_not_promoted_without_evidence():

    service = (
        KnowledgePromotionService()
    )

    updated = service.promote_observation(
        make_observation()
    )

    assert (
        updated.state
        is KnowledgeState.OBSERVATION
    )


def test_promoted_with_evidence():

    service = (
        KnowledgePromotionService()
    )

    updated = service.promote_observation(
        make_observation(
            evidence=1
        )
    )

    assert (
        updated.state
        is KnowledgeState.HYPOTHESIS
    )
