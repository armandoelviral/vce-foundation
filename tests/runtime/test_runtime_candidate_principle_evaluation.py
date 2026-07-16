from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def make_candidate_principle(
    *,
    evidence_count: int = 5,
    independent_validations: int = 3,
    destruction_attempts: int = 5,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="CP-001",
        title="Candidate principle",
        state=KnowledgeState.CANDIDATE_PRINCIPLE,
        evidence_count=evidence_count,
        independent_validations=independent_validations,
        destruction_attempts=destruction_attempts,
    )


def test_runtime_advances_eligible_candidate_principle() -> None:
    result = KnowledgeRuntime().evaluate_candidate_principle(
        make_candidate_principle(),
    )

    assert result.transition_executed is True
    assert result.artifact.state is KnowledgeState.PRINCIPLE


def test_runtime_rejects_ineligible_candidate_principle() -> None:
    artifact = make_candidate_principle(
        independent_validations=2,
    )

    result = KnowledgeRuntime().evaluate_candidate_principle(
        artifact,
    )

    assert result.transition_executed is False
    assert result.artifact is artifact
    assert result.artifact.state is KnowledgeState.CANDIDATE_PRINCIPLE


def test_runtime_does_not_mutate_candidate_principle() -> None:
    artifact = make_candidate_principle()

    KnowledgeRuntime().evaluate_candidate_principle(
        artifact,
    )

    assert artifact.state is KnowledgeState.CANDIDATE_PRINCIPLE
