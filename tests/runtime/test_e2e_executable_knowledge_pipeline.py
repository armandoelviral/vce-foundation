from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_history import KnowledgeHistory
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


def test_complete_pipeline():

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Executable Knowledge",
        state=KnowledgeState.OBSERVATION,
    )

    runtime = KnowledgeRuntime()

    result = runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    history = (
        KnowledgeHistoryRecorder()
        .record(
            KnowledgeHistory(),
            result,
        )
    )

    replay = (
        KnowledgeReplay()
        .replay(
            history,
            "OBS-001",
        )
    )

    assert (
        replay
        is KnowledgeState.HYPOTHESIS
    )

    assert len(history) == 1

    assert (
        history.events[0].event_id
        == "EVT-001"
    )
