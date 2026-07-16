from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event import RuntimeEvent
from has.runtime.runtime_event_verifier import (
    RuntimeEventVerifier,
)


def make_event(
    *,
    event_id: str = "EVT-001",
    artifact_id: str = "K-001",
    from_state: KnowledgeState = KnowledgeState.OBSERVATION,
    to_state: KnowledgeState = KnowledgeState.HYPOTHESIS,
    eligible: bool = True,
) -> RuntimeEvent:
    evaluation = (
        EvaluationResult(
            eligible=True,
        )
        if eligible
        else EvaluationResult(
            eligible=False,
            reasons=("insufficient_evidence",),
        )
    )

    return RuntimeEvent(
        event_id=event_id,
        artifact_id=artifact_id,
        from_state=from_state,
        to_state=to_state,
        evaluation=evaluation,
    )


def test_accepts_valid_runtime_event() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(),
    )

    assert result.valid is True
    assert result.reasons == ()


def test_rejects_skipped_transition() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            from_state=KnowledgeState.OBSERVATION,
            to_state=KnowledgeState.PRINCIPLE,
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "transition_not_allowed",
    )


def test_rejects_backward_transition() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            from_state=KnowledgeState.PRINCIPLE,
            to_state=KnowledgeState.OBSERVATION,
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "transition_not_allowed",
    )


def test_rejects_empty_event_id() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            event_id="",
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "event_id_required",
    )


def test_rejects_blank_artifact_id() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            artifact_id="   ",
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "artifact_id_required",
    )


def test_rejects_ineligible_evaluation() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            eligible=False,
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "eligible_evaluation_required",
    )


def test_reports_all_detected_failures() -> None:
    result = RuntimeEventVerifier().verify(
        make_event(
            event_id="",
            artifact_id="",
            from_state=KnowledgeState.PRINCIPLE,
            to_state=KnowledgeState.OBSERVATION,
            eligible=False,
        ),
    )

    assert result.valid is False
    assert result.reasons == (
        "event_id_required",
        "artifact_id_required",
        "eligible_evaluation_required",
        "transition_not_allowed",
    )
