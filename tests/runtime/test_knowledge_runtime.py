from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def test_runtime_records_observation() -> None:
    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    result = runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    assert result.transition_executed is True
    assert result.artifact.state is KnowledgeState.HYPOTHESIS
    assert result.artifact.evidence_count == 1

    assert result.event is not None
    assert result.event.event_id == "EVT-001"
    assert result.event.artifact_id == "OBS-001"
    assert (
        result.event.from_state
        is KnowledgeState.OBSERVATION
    )
    assert (
        result.event.to_state
        is KnowledgeState.HYPOTHESIS
    )
