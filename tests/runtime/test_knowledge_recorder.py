from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_recorder import (
    KnowledgeRecorder,
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


def runtime_event():
    return RuntimeEvent(
        event_id="EVT-001",
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_records_runtime_event():

    recorder = KnowledgeRecorder()

    history = recorder.record(
        KnowledgeHistory(),
        RuntimeResult(
            artifact=artifact(),
            transition_executed=True,
            event=runtime_event(),
        ),
    )

    assert len(history) == 1

    assert (
        history.events[0].event_id
        == "EVT-001"
    )


def test_no_event_keeps_history():

    recorder = KnowledgeRecorder()

    history = KnowledgeHistory()

    updated = recorder.record(
        history,
        RuntimeResult(
            artifact=artifact(),
            transition_executed=False,
            event=None,
        ),
    )

    assert updated is history
