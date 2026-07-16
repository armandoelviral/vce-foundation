from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.promotion_requirements import PromotionRequirements
from has.runtime.requirements_promotion_policy import (
    RequirementsPromotionPolicy,
)


def make_hypothesis(
    *,
    evidence_count: int = 0,
    independent_validations: int = 0,
    destruction_attempts: int = 0,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="H-001",
        title="Candidate hypothesis",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=evidence_count,
        independent_validations=independent_validations,
        destruction_attempts=destruction_attempts,
    )


def make_policy() -> RequirementsPromotionPolicy:
    return RequirementsPromotionPolicy(
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=PromotionRequirements(
            minimum_evidence=3,
            minimum_independent_validations=1,
            minimum_destruction_attempts=2,
        ),
    )


def test_accepts_artifact_meeting_all_requirements() -> None:
    artifact = make_hypothesis(
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=2,
    )

    assert make_policy().can_promote(artifact) is True


def test_rejects_insufficient_evidence() -> None:
    artifact = make_hypothesis(
        evidence_count=2,
        independent_validations=1,
        destruction_attempts=2,
    )

    assert make_policy().can_promote(artifact) is False


def test_rejects_insufficient_independent_validation() -> None:
    artifact = make_hypothesis(
        evidence_count=3,
        independent_validations=0,
        destruction_attempts=2,
    )

    assert make_policy().can_promote(artifact) is False


def test_rejects_insufficient_destruction_attempts() -> None:
    artifact = make_hypothesis(
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=1,
    )

    assert make_policy().can_promote(artifact) is False


def test_rejects_wrong_source_state() -> None:
    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
        evidence_count=100,
        independent_validations=100,
        destruction_attempts=100,
    )

    assert make_policy().can_promote(artifact) is False


def test_zero_requirements_still_require_correct_state() -> None:
    policy = RequirementsPromotionPolicy(
        source_state=KnowledgeState.OBSERVATION,
        requirements=PromotionRequirements(),
    )

    observation = KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
    )

    hypothesis = KnowledgeArtifact(
        identifier="H-001",
        title="Hypothesis",
        state=KnowledgeState.HYPOTHESIS,
    )

    assert policy.can_promote(observation) is True
    assert policy.can_promote(hypothesis) is False
