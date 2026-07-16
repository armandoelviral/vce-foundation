from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_runtime_never_mutates_input():

    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Immutable",
        state=KnowledgeState.OBSERVATION,
    )

    runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    assert (
        artifact.state
        is KnowledgeState.OBSERVATION
    )

    assert artifact.evidence_count == 0

    assert (
        artifact.independent_validations
        == 0
    )

    assert (
        artifact.destruction_attempts
        == 0
    )
