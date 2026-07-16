from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_history_query import (
    KnowledgeHistoryQuery,
)
from has.runtime.knowledge_history_recorder import (
    KnowledgeHistoryRecorder,
)
from has.runtime.knowledge_replay import (
    KnowledgeReplay,
)
from has.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_rejected_pipeline_preserves_history():

    runtime = KnowledgeRuntime()

    recorder = KnowledgeHistoryRecorder()

    replay = KnowledgeReplay()

    query = KnowledgeHistoryQuery()

    history = KnowledgeHistory()

    #
    # Paso 1
    #

    observation = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    accepted = runtime.record_observation(
        observation,
        event_id="EVT-001",
    )

    history = recorder.record(
        history,
        accepted,
    )

    #
    # Paso 2 (rechazado)
    #

    hypothesis = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.HYPOTHESIS,
        evidence_count=1,
        independent_validations=0,
        destruction_attempts=0,
    )

    rejected = runtime.evaluate_hypothesis(
        hypothesis,
        event_id="EVT-002",
    )

    assert rejected.transition_executed is False

    assert rejected.event is None

    #
    # El recorder NO debe modificar historia.
    #

    updated_history = recorder.record(
        history,
        rejected,
    )

    assert updated_history is history

    #
    # Sigue existiendo un solo evento.
    #

    events = query.by_artifact(
        history,
        "OBS-001",
    )

    assert len(events) == 1

    assert events[0].event_id == "EVT-001"

    #
    # Replay mantiene el último estado válido.
    #

    reconstructed = replay.replay(
        history,
        "OBS-001",
    )

    assert reconstructed is KnowledgeState.HYPOTHESIS
