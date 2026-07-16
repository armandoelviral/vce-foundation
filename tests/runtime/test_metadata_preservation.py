from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.state_transition import StateTransition


def test_state_transition_preserves_metadata() -> None:
    metadata = {
        "source": "laboratory",
        "review_status": "pending",
    }

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
        metadata=metadata,
    )

    updated = StateTransition().apply(
        artifact,
        KnowledgeState.HYPOTHESIS,
    )

    assert updated.state is KnowledgeState.HYPOTHESIS
    assert updated.metadata == metadata
