from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_history_query import (
    KnowledgeHistoryQuery,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def event(
    event_id: str,
    artifact: str,
):

    return RuntimeEvent(
        event_id=event_id,
        artifact_id=artifact,
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def history():

    return (
        KnowledgeHistory()
        .append(event("EVT-001","OBS-001"))
        .append(event("EVT-002","OBS-002"))
        .append(event("EVT-003","OBS-001"))
    )


def test_latest():

    latest = (
        KnowledgeHistoryQuery()
        .latest(
            history(),
        )
    )

    assert latest.event_id == "EVT-003"


def test_by_artifact():

    events = (
        KnowledgeHistoryQuery()
        .by_artifact(
            history(),
            "OBS-001",
        )
    )

    assert len(events) == 2


def test_count():

    assert (
        KnowledgeHistoryQuery()
        .count(
            history(),
        )
        == 3
    )


def test_latest_empty():

    assert (
        KnowledgeHistoryQuery()
        .latest(
            KnowledgeHistory(),
        )
        is None
    )
