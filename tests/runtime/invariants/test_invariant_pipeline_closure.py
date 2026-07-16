from collections.abc import Callable

from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_history_recorder import (
    KnowledgeHistoryRecorder,
)
from has.runtime.knowledge_replay import KnowledgeReplay
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event_verifier import (
    RuntimeEventVerifier,
)
from has.runtime.runtime_result import RuntimeResult


RuntimeOperation = Callable[
    [KnowledgeArtifact, str],
    RuntimeResult,
]


def execute_record_observation(
    runtime: KnowledgeRuntime,
    artifact: KnowledgeArtifact,
    event_id: str,
) -> RuntimeResult:
    return runtime.record_observation(
        artifact,
        event_id=event_id,
    )


def execute_evaluate_hypothesis(
    runtime: KnowledgeRuntime,
    artifact: KnowledgeArtifact,
    event_id: str,
) -> RuntimeResult:
    return runtime.evaluate_hypothesis(
        artifact,
        event_id=event_id,
    )


def execute_evaluate_candidate_principle(
    runtime: KnowledgeRuntime,
    artifact: KnowledgeArtifact,
    event_id: str,
) -> RuntimeResult:
    return runtime.evaluate_candidate_principle(
        artifact,
        event_id=event_id,
    )


def assert_pipeline_closure(
    *,
    artifact: KnowledgeArtifact,
    event_id: str,
    operation: Callable[
        [KnowledgeRuntime, KnowledgeArtifact, str],
        RuntimeResult,
    ],
    expected_state: KnowledgeState,
) -> None:
    runtime = KnowledgeRuntime()

    result = operation(
        runtime,
        artifact,
        event_id,
    )

    assert result.transition_executed is True
    assert result.artifact.state is expected_state
    assert result.event is not None

    verification = RuntimeEventVerifier().verify(
        result.event,
    )

    assert verification.valid is True
    assert verification.reasons == ()

    history = KnowledgeHistoryRecorder().record(
        KnowledgeHistory(),
        result,
    )

    reconstructed_state = KnowledgeReplay().replay(
        history,
        artifact.identifier,
    )

    assert reconstructed_state is result.artifact.state
    assert reconstructed_state is expected_state


def test_observation_pipeline_is_closed() -> None:
    artifact = KnowledgeArtifact(
        identifier="K-001",
        title="Observation closure",
        state=KnowledgeState.OBSERVATION,
    )

    assert_pipeline_closure(
        artifact=artifact,
        event_id="EVT-001",
        operation=execute_record_observation,
        expected_state=KnowledgeState.HYPOTHESIS,
    )


def test_hypothesis_pipeline_is_closed() -> None:
    artifact = KnowledgeArtifact(
        identifier="K-002",
        title="Hypothesis closure",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=2,
    )

    assert_pipeline_closure(
        artifact=artifact,
        event_id="EVT-002",
        operation=execute_evaluate_hypothesis,
        expected_state=KnowledgeState.CANDIDATE_PRINCIPLE,
    )


def test_candidate_principle_pipeline_is_closed() -> None:
    artifact = KnowledgeArtifact(
        identifier="K-003",
        title="Principle closure",
        state=KnowledgeState.CANDIDATE_PRINCIPLE,
        evidence_count=5,
        independent_validations=3,
        destruction_attempts=5,
    )

    assert_pipeline_closure(
        artifact=artifact,
        event_id="EVT-003",
        operation=execute_evaluate_candidate_principle,
        expected_state=KnowledgeState.PRINCIPLE,
    )
