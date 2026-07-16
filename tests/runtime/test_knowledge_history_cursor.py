from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_history_cursor import (
    KnowledgeHistoryCursor,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def event(
    event_id: str,
):

    return RuntimeEvent(
        event_id=event_id,
        artifact_id="OBS",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def history():

    return (
        KnowledgeHistory()
        .append(event("EVT-001"))
        .append(event("EVT-002"))
        .append(event("EVT-003"))
    )


def test_iteration():

    cursor = (
        KnowledgeHistoryCursor(
            history(),
        )
    )

    assert cursor.has_next()

    assert (
        cursor.next().event_id
        == "EVT-001"
    )

    assert (
        cursor.next().event_id
        == "EVT-002"
    )

    assert (
        cursor.next().event_id
        == "EVT-003"
    )

    assert (
        cursor.has_next()
        is False
    )


def test_reset():

    cursor = (
        KnowledgeHistoryCursor(
            history(),
        )
    )

    cursor.next()

    cursor.reset()

    assert (
        cursor.next().event_id
        == "EVT-001"
    )
