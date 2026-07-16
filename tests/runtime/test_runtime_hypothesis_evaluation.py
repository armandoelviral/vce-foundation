from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def make_hypothesis(
    *,
    evidence_count: int = 3,
    independent_validations: int = 1,
    destruction_attempts: int = 2,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="H-001",
        title="Candidate hypothesis",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=evidence_count,
        independent_validations=independent_validations,
        destruction_attempts=destruction_attempts,
    )


def test_runtime_advances_eligible_hypothesis() -> None:
    result = KnowledgeRuntime().evaluate_hypothesis(
        make_hypothesis(),
    )

    assert result.transition_executed is True
    assert (
        result.artifact.state
        is KnowledgeState.CANDIDATE_PRINCIPLE
    )


def test_runtime_rejects_ineligible_hypothesis() -> None:
    artifact = make_hypothesis(
        independent_validations=0,
    )

    result = KnowledgeRuntime().evaluate_hypothesis(
        artifact,
    )

    assert result.transition_executed is False
    assert result.artifact is artifact
    assert result.artifact.state is KnowledgeState.HYPOTHESIS


def test_runtime_does_not_mutate_hypothesis() -> None:
    artifact = make_hypothesis()

    KnowledgeRuntime().evaluate_hypothesis(
        artifact,
    )

    assert artifact.state is KnowledgeState.HYPOTHESIS
