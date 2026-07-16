from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def test_runtime_event_defaults() -> None:

    event = RuntimeEvent(
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )

    assert event.artifact_id == "OBS-001"

    assert (
        event.from_state
        is KnowledgeState.OBSERVATION
    )

    assert (
        event.to_state
        is KnowledgeState.HYPOTHESIS
    )

    assert event.evaluation.eligible is True
