import pytest

from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.observation_promotion_policy import (
    ObservationPromotionPolicy,
)


def make_artifact(
    *,
    state: KnowledgeState = KnowledgeState.OBSERVATION,
    evidence_count: int = 0,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example observation",
        state=state,
        evidence_count=evidence_count,
    )


def test_rejects_observation_without_evidence() -> None:
    policy = ObservationPromotionPolicy()

    assert policy.can_promote(make_artifact()) is False


def test_accepts_observation_with_required_evidence() -> None:
    policy = ObservationPromotionPolicy()

    assert (
        policy.can_promote(
            make_artifact(evidence_count=1),
        )
        is True
    )


def test_rejects_artifact_in_wrong_state() -> None:
    policy = ObservationPromotionPolicy()

    artifact = make_artifact(
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=10,
    )

    assert policy.can_promote(artifact) is False


def test_supports_configurable_evidence_threshold() -> None:
    policy = ObservationPromotionPolicy(minimum_evidence=3)

    assert policy.can_promote(make_artifact(evidence_count=2)) is False
    assert policy.can_promote(make_artifact(evidence_count=3)) is True


def test_rejects_invalid_threshold() -> None:
    with pytest.raises(
        ValueError,
        match="minimum_evidence must be at least 1",
    ):
        ObservationPromotionPolicy(minimum_evidence=0)
