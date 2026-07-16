from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def make_observation() -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )


def test_runtime_returns_runtime_result() -> None:
    result = KnowledgeRuntime().record_observation(
        make_observation(),
        event_id="EVT-001",
    )

    assert hasattr(result, "artifact")
    assert hasattr(result, "transition_executed")
    assert hasattr(result, "event")


def test_runtime_never_mutates_input() -> None:
    runtime = KnowledgeRuntime()
    artifact = make_observation()

    runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    assert artifact.state is KnowledgeState.OBSERVATION
    assert artifact.evidence_count == 0


def test_runtime_is_deterministic() -> None:
    runtime = KnowledgeRuntime()
    artifact = make_observation()

    first = runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )
    second = runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    assert first == second
