from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def test_runtime_event():

    event = RuntimeEvent(
        event_id="EVT-001",
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )

    assert event.event_id == "EVT-001"

    assert event.artifact_id == "OBS-001"

    assert (
        event.from_state
        is KnowledgeState.OBSERVATION
    )

    assert (
        event.to_state
        is KnowledgeState.HYPOTHESIS
    )

    assert event.evaluation.eligible
