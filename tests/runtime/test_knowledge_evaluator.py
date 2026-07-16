from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_evaluator import KnowledgeEvaluator
from has.runtime.knowledge_state import KnowledgeState


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


def requirements() -> EvaluationRequirements:
    return EvaluationRequirements(
        minimum_evidence=3,
        minimum_independent_validations=1,
        minimum_destruction_attempts=2,
    )


def test_accepts_artifact_meeting_all_requirements() -> None:
    artifact = make_hypothesis(
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=2,
    )

    result = KnowledgeEvaluator().evaluate(
        artifact,
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is True
    assert result.reasons == ()


def test_explains_insufficient_evidence() -> None:
    result = KnowledgeEvaluator().evaluate(
        make_hypothesis(
            evidence_count=2,
            independent_validations=1,
            destruction_attempts=2,
        ),
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is False
    assert result.reasons == ("insufficient_evidence",)


def test_explains_missing_independent_validation() -> None:
    result = KnowledgeEvaluator().evaluate(
        make_hypothesis(
            evidence_count=3,
            independent_validations=0,
            destruction_attempts=2,
        ),
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is False
    assert result.reasons == (
        "insufficient_independent_validations",
    )


def test_explains_insufficient_destruction_attempts() -> None:
    result = KnowledgeEvaluator().evaluate(
        make_hypothesis(
            evidence_count=3,
            independent_validations=1,
            destruction_attempts=1,
        ),
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is False
    assert result.reasons == (
        "insufficient_destruction_attempts",
    )


def test_explains_wrong_source_state() -> None:
    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=2,
    )

    result = KnowledgeEvaluator().evaluate(
        artifact,
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is False
    assert result.reasons == ("wrong_source_state",)


def test_reports_all_failed_requirements() -> None:
    result = KnowledgeEvaluator().evaluate(
        make_hypothesis(),
        source_state=KnowledgeState.HYPOTHESIS,
        requirements=requirements(),
    )

    assert result.eligible is False
    assert result.reasons == (
        "insufficient_evidence",
        "insufficient_independent_validations",
        "insufficient_destruction_attempts",
    )
