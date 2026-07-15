from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def test_defaults():

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    assert artifact.evidence_count == 0

    assert artifact.destruction_attempts == 0

    assert artifact.independent_validations == 0
