from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def test_runtime_returns_runtime_result() -> None:
    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    result = runtime.record_observation(artifact)

    assert hasattr(result, "artifact")
    assert hasattr(result, "transition_executed")


def test_runtime_never_mutates_input() -> None:
    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    runtime.record_observation(artifact)

    assert artifact.state is KnowledgeState.OBSERVATION
    assert artifact.evidence_count == 0


def test_runtime_is_deterministic() -> None:
    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    first = runtime.record_observation(artifact)
    second = runtime.record_observation(artifact)

    assert first == second
