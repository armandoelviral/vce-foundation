from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_runtime_records_observation():

    runtime = KnowledgeRuntime()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    updated = runtime.record_observation(
        artifact
    )

    assert (
        updated.state
        is KnowledgeState.HYPOTHESIS
    )

    assert updated.evidence_count == 1
