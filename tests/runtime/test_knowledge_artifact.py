from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState


def make_artifact(
    *,
    metadata: dict[str, object] | None = None,
) -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
        metadata=metadata or {},
    )


def test_defaults() -> None:
    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    assert artifact.evidence_count == 0
    assert artifact.destruction_attempts == 0
    assert artifact.independent_validations == 0
    assert artifact.metadata == {}


def test_accepts_custom_metadata() -> None:
    artifact = make_artifact(
        metadata={
            "source": "laboratory",
            "reproducibility": "pending",
        },
    )

    assert artifact.metadata["source"] == "laboratory"
    assert artifact.metadata["reproducibility"] == "pending"


def test_artifacts_do_not_share_default_metadata() -> None:
    first = make_artifact()
    second = make_artifact()

    assert first.metadata is not second.metadata
