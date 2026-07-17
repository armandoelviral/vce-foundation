from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)
from has.runtime.runtime_result import (
    RuntimeResult,
)


def artifact() -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )


def event() -> RuntimeEvent:
    return RuntimeEvent(
        event_id="EVT-001",
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_runtime_result_without_event() -> None:
    result = RuntimeResult(
        artifact=artifact(),
        transition_executed=False,
    )

    assert result.event is None


def test_runtime_result_with_event() -> None:
    result = RuntimeResult(
        artifact=artifact(),
        transition_executed=True,
        event=event(),
    )

    assert result.event is not None
    assert result.event.event_id == "EVT-001"
