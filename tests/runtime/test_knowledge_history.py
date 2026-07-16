import pytest

from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event import RuntimeEvent


def make_event(
    *,
    event_id: str,
    artifact_id: str = "OBS-001",
    from_state: KnowledgeState = KnowledgeState.OBSERVATION,
    to_state: KnowledgeState = KnowledgeState.HYPOTHESIS,
) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=event_id,
        artifact_id=artifact_id,
        from_state=from_state,
        to_state=to_state,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_history_starts_empty() -> None:
    history = KnowledgeHistory()

    assert history.events == ()
    assert len(history) == 0


def test_append_returns_new_history() -> None:
    history = KnowledgeHistory()
    event = make_event(event_id="EVT-001")

    updated = history.append(event)

    assert len(history) == 0
    assert len(updated) == 1
    assert updated.events == (event,)


def test_history_preserves_event_order() -> None:
    first = make_event(event_id="EVT-001")
    second = make_event(
        event_id="EVT-002",
        artifact_id="H-001",
        from_state=KnowledgeState.HYPOTHESIS,
        to_state=KnowledgeState.CANDIDATE_PRINCIPLE,
    )

    history = (
        KnowledgeHistory()
        .append(first)
        .append(second)
    )

    assert history.events == (
        first,
        second,
    )


def test_contains_event_id() -> None:
    history = KnowledgeHistory().append(
        make_event(event_id="EVT-001"),
    )

    assert history.contains("EVT-001") is True
    assert history.contains("EVT-999") is False


def test_rejects_duplicate_event_id() -> None:
    history = KnowledgeHistory().append(
        make_event(event_id="EVT-001"),
    )

    with pytest.raises(
        ValueError,
        match="event_id already exists: EVT-001",
    ):
        history.append(
            make_event(
                event_id="EVT-001",
                artifact_id="OBS-002",
            ),
        )
