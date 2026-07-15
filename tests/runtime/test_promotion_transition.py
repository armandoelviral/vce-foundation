from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)
from has.runtime.transitions.promotion_transition import (
    PromotionTransition,
)


def make_observation(
    *,
    evidence_count: int,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example observation",
        state=KnowledgeState.OBSERVATION,
        evidence_count=evidence_count,
    )


def make_transition() -> PromotionTransition:
    return PromotionTransition(
        policy=ObservationPromotionPolicy(),
        promoter=KnowledgePromoter(),
        target_state=KnowledgeState.HYPOTHESIS,
    )


def test_promotes_when_policy_accepts() -> None:
    result = make_transition().execute(
        make_observation(evidence_count=1),
    )

    assert result.state is KnowledgeState.HYPOTHESIS


def test_returns_artifact_unchanged_when_policy_rejects() -> None:
    artifact = make_observation(evidence_count=0)

    result = make_transition().execute(artifact)

    assert result is artifact
    assert result.state is KnowledgeState.OBSERVATION
