import pytest

from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_replay import KnowledgeReplay
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event import RuntimeEvent


def make_event(
    *,
    event_id: str,
    from_state: KnowledgeState,
    to_state: KnowledgeState,
) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=event_id,
        artifact_id="K-001",
        from_state=from_state,
        to_state=to_state,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_continuous_event_chain_replays_successfully() -> None:
    history = (
        KnowledgeHistory()
        .append(
            make_event(
                event_id="EVT-001",
                from_state=KnowledgeState.OBSERVATION,
                to_state=KnowledgeState.HYPOTHESIS,
            ),
        )
        .append(
            make_event(
                event_id="EVT-002",
                from_state=KnowledgeState.HYPOTHESIS,
                to_state=KnowledgeState.CANDIDATE_PRINCIPLE,
            ),
        )
        .append(
            make_event(
                event_id="EVT-003",
                from_state=KnowledgeState.CANDIDATE_PRINCIPLE,
                to_state=KnowledgeState.PRINCIPLE,
            ),
        )
    )

    result = KnowledgeReplay().replay(
        history,
        "K-001",
    )

    assert result is KnowledgeState.PRINCIPLE


def test_discontinuous_event_chain_is_rejected() -> None:
    history = (
        KnowledgeHistory()
        .append(
            make_event(
                event_id="EVT-001",
                from_state=KnowledgeState.OBSERVATION,
                to_state=KnowledgeState.HYPOTHESIS,
            ),
        )
        .append(
            make_event(
                event_id="EVT-002",
                from_state=KnowledgeState.CANDIDATE_PRINCIPLE,
                to_state=KnowledgeState.PRINCIPLE,
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="discontinuous knowledge history for artifact: K-001",
    ):
        KnowledgeReplay().replay(
            history,
            "K-001",
        )
