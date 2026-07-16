import pytest

from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_history_recorder import (
    KnowledgeHistoryRecorder,
)
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event import RuntimeEvent
from has.runtime.runtime_event_verifier import RuntimeEventVerifier
from has.runtime.runtime_result import RuntimeResult


def make_artifact() -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="K-001",
        title="History integrity",
        state=KnowledgeState.HYPOTHESIS,
    )


def make_valid_event(
    *,
    event_id: str = "EVT-001",
) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=event_id,
        artifact_id="K-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.HYPOTHESIS,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def make_invalid_event() -> RuntimeEvent:
    return RuntimeEvent(
        event_id="EVT-INVALID",
        artifact_id="K-001",
        from_state=KnowledgeState.OBSERVATION,
        to_state=KnowledgeState.PRINCIPLE,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_every_stored_event_is_semantically_valid() -> None:
    history = KnowledgeHistory().append(
        make_valid_event(),
    )

    verifier = RuntimeEventVerifier()

    results = tuple(
        verifier.verify(event)
        for event in history.events
    )

    assert all(
        result.valid
        for result in results
    )


def test_recorder_rejects_invalid_event_before_storage() -> None:
    history = KnowledgeHistory()

    result = RuntimeResult(
        artifact=make_artifact(),
        transition_executed=True,
        event=make_invalid_event(),
    )

    with pytest.raises(
        ValueError,
        match="transition_not_allowed",
    ):
        KnowledgeHistoryRecorder().record(
            history,
            result,
        )

    assert len(history) == 0
