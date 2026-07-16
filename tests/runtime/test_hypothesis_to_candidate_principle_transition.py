from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.transitions.hypothesis_to_candidate_principle_transition import (
    HypothesisToCandidatePrincipleTransition,
)


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


def test_advances_eligible_hypothesis() -> None:
    transition = HypothesisToCandidatePrincipleTransition()

    result = transition.execute(
        make_hypothesis(),
    )

    assert result.state is KnowledgeState.CANDIDATE_PRINCIPLE
    assert result.evidence_count == 3
    assert result.independent_validations == 1
    assert result.destruction_attempts == 2


def test_rejects_insufficient_evidence() -> None:
    artifact = make_hypothesis(evidence_count=2)

    result = HypothesisToCandidatePrincipleTransition().execute(
        artifact,
    )

    assert result is artifact
    assert result.state is KnowledgeState.HYPOTHESIS


def test_rejects_insufficient_independent_validation() -> None:
    artifact = make_hypothesis(
        independent_validations=0,
    )

    result = HypothesisToCandidatePrincipleTransition().execute(
        artifact,
    )

    assert result is artifact


def test_rejects_insufficient_destruction_attempts() -> None:
    artifact = make_hypothesis(
        destruction_attempts=1,
    )

    result = HypothesisToCandidatePrincipleTransition().execute(
        artifact,
    )

    assert result is artifact


def test_rejects_wrong_source_state() -> None:
    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
        evidence_count=100,
        independent_validations=100,
        destruction_attempts=100,
    )

    result = HypothesisToCandidatePrincipleTransition().execute(
        artifact,
    )

    assert result is artifact
    assert result.state is KnowledgeState.OBSERVATION


def test_accepts_custom_requirements() -> None:
    transition = HypothesisToCandidatePrincipleTransition(
        requirements=EvaluationRequirements(
            minimum_evidence=1,
            minimum_independent_validations=0,
            minimum_destruction_attempts=0,
        ),
    )

    result = transition.execute(
        make_hypothesis(
            evidence_count=1,
            independent_validations=0,
            destruction_attempts=0,
        ),
    )

    assert result.state is KnowledgeState.CANDIDATE_PRINCIPLE
