from has.runtime.evidence_accumulator import EvidenceAccumulator
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.transitions.evidence_recording_transition import (
    EvidenceRecordingTransition,
)


def make_observation() -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Example observation",
        state=KnowledgeState.OBSERVATION,
    )


def test_records_evidence_without_changing_state() -> None:
    transition = EvidenceRecordingTransition(
        EvidenceAccumulator(),
    )

    result = transition.execute(make_observation())

    assert result.state is KnowledgeState.OBSERVATION
    assert result.evidence_count == 1


def test_does_not_mutate_original_artifact() -> None:
    transition = EvidenceRecordingTransition(
        EvidenceAccumulator(),
    )
    artifact = make_observation()

    result = transition.execute(artifact)

    assert artifact.evidence_count == 0
    assert result.evidence_count == 1
