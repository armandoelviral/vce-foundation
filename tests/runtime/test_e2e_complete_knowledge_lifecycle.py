from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_history_query import KnowledgeHistoryQuery
from has.runtime.knowledge_history_recorder import (
    KnowledgeHistoryRecorder,
)
from has.runtime.knowledge_replay import KnowledgeReplay
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState


def test_complete_knowledge_lifecycle() -> None:
    runtime = KnowledgeRuntime()
    recorder = KnowledgeHistoryRecorder()
    query = KnowledgeHistoryQuery()
    replay = KnowledgeReplay()

    original_observation = KnowledgeArtifact(
        identifier="K-001",
        title="Executable knowledge lifecycle",
        state=KnowledgeState.OBSERVATION,
    )

    hypothesis_result = runtime.record_observation(
        original_observation,
        event_id="EVT-001",
    )

    assert hypothesis_result.transition_executed is True
    assert (
        hypothesis_result.artifact.state
        is KnowledgeState.HYPOTHESIS
    )
    assert hypothesis_result.event is not None

    history = recorder.record(
        KnowledgeHistory(),
        hypothesis_result,
    )

    hypothesis = KnowledgeArtifact(
        identifier="K-001",
        title="Executable knowledge lifecycle",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=3,
        independent_validations=1,
        destruction_attempts=2,
    )

    candidate_result = runtime.evaluate_hypothesis(
        hypothesis,
        event_id="EVT-002",
    )

    assert candidate_result.transition_executed is True
    assert (
        candidate_result.artifact.state
        is KnowledgeState.CANDIDATE_PRINCIPLE
    )
    assert candidate_result.event is not None

    history = recorder.record(
        history,
        candidate_result,
    )

    candidate_principle = KnowledgeArtifact(
        identifier="K-001",
        title="Executable knowledge lifecycle",
        state=KnowledgeState.CANDIDATE_PRINCIPLE,
        evidence_count=5,
        independent_validations=3,
        destruction_attempts=5,
    )

    principle_result = runtime.evaluate_candidate_principle(
        candidate_principle,
        event_id="EVT-003",
    )

    assert principle_result.transition_executed is True
    assert (
        principle_result.artifact.state
        is KnowledgeState.PRINCIPLE
    )
    assert principle_result.event is not None

    history = recorder.record(
        history,
        principle_result,
    )

    events = query.by_artifact(
        history,
        "K-001",
    )

    assert len(events) == 3

    assert tuple(
        event.event_id
        for event in events
    ) == (
        "EVT-001",
        "EVT-002",
        "EVT-003",
    )

    assert tuple(
        event.from_state
        for event in events
    ) == (
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
    )

    assert tuple(
        event.to_state
        for event in events
    ) == (
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
        KnowledgeState.PRINCIPLE,
    )

    reconstructed_state = replay.replay(
        history,
        "K-001",
    )

    assert reconstructed_state is KnowledgeState.PRINCIPLE

    assert original_observation.state is KnowledgeState.OBSERVATION
    assert original_observation.evidence_count == 0
    assert hypothesis.state is KnowledgeState.HYPOTHESIS
    assert candidate_principle.state is KnowledgeState.CANDIDATE_PRINCIPLE
