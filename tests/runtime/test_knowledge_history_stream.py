from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_history_stream import (
    KnowledgeHistoryStream,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def make_event(event_id: str) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=event_id,
        artifact_id="OBS-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_empty_stream() -> None:
    history = KnowledgeHistory()

    assert list(
        KnowledgeHistoryStream().stream(
            history,
        )
    ) == []


def test_stream_preserves_order() -> None:
    history = (
        KnowledgeHistory()
        .append(make_event("EVT-001"))
        .append(make_event("EVT-002"))
        .append(make_event("EVT-003"))
    )

    events = list(
        KnowledgeHistoryStream().stream(
            history,
        )
    )

    assert [
        event.event_id
        for event in events
    ] == [
        "EVT-001",
        "EVT-002",
        "EVT-003",
    ]
