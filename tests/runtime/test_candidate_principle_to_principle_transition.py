from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.transitions.candidate_principle_to_principle_transition import (
    CandidatePrincipleToPrincipleTransition,
)


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


def test_advances_eligible_candidate_principle() -> None:
    artifact = make_candidate_principle()

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert result.state is KnowledgeState.PRINCIPLE
    assert result.evidence_count == 5
    assert result.independent_validations == 3
    assert result.destruction_attempts == 5


def test_does_not_mutate_original_artifact() -> None:
    artifact = make_candidate_principle()

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert artifact.state is KnowledgeState.CANDIDATE_PRINCIPLE
    assert result.state is KnowledgeState.PRINCIPLE


def test_rejects_insufficient_evidence() -> None:
    artifact = make_candidate_principle(
        evidence_count=4,
    )

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert result is artifact
    assert result.state is KnowledgeState.CANDIDATE_PRINCIPLE


def test_rejects_insufficient_independent_validations() -> None:
    artifact = make_candidate_principle(
        independent_validations=2,
    )

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert result is artifact


def test_rejects_insufficient_destruction_attempts() -> None:
    artifact = make_candidate_principle(
        destruction_attempts=4,
    )

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert result is artifact


def test_rejects_wrong_source_state() -> None:
    artifact = KnowledgeArtifact(
        identifier="H-001",
        title="Hypothesis",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=100,
        independent_validations=100,
        destruction_attempts=100,
    )

    result = CandidatePrincipleToPrincipleTransition().execute(
        artifact,
    )

    assert result is artifact
    assert result.state is KnowledgeState.HYPOTHESIS


def test_accepts_custom_requirements() -> None:
    transition = CandidatePrincipleToPrincipleTransition(
        requirements=EvaluationRequirements(
            minimum_evidence=1,
            minimum_independent_validations=0,
            minimum_destruction_attempts=0,
        ),
    )

    result = transition.execute(
        make_candidate_principle(
            evidence_count=1,
            independent_validations=0,
            destruction_attempts=0,
        ),
    )

    assert result.state is KnowledgeState.PRINCIPLE
