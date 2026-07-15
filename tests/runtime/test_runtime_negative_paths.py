from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def test_hypothesis_is_not_promoted_again() -> None:

    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="H-001",
        title="Already hypothesis",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=10,
    )

    result = runtime.record_observation(
        artifact
    )

    assert result.transition_executed is False

    assert result.artifact.state is KnowledgeState.HYPOTHESIS

    assert result.artifact.evidence_count == 10
