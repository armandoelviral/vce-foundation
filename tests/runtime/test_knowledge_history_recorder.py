from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_history_recorder import (
    KnowledgeHistoryRecorder,
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


def artifact():
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.HYPOTHESIS,
    )


def event():
    return RuntimeEvent(
        event_id="EVT-001",
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_records_event():

    history = KnowledgeHistory()

    result = RuntimeResult(
        artifact=artifact(),
        transition_executed=True,
        event=event(),
    )

    updated = (
        KnowledgeHistoryRecorder()
        .record(
            history,
            result,
        )
    )

    assert len(history) == 0

    assert len(updated) == 1

    assert (
        updated.events[0].event_id
        == "EVT-001"
    )


def test_ignores_none_event():

    history = KnowledgeHistory()

    result = RuntimeResult(
        artifact=artifact(),
        transition_executed=False,
        event=None,
    )

    updated = (
        KnowledgeHistoryRecorder()
        .record(
            history,
            result,
        )
    )

    assert updated is history
