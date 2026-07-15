import pytest

from has.runtime.evidence_accumulator import (
    EvidenceAccumulator,
)
from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def make_artifact():

    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
    )


def test_adds_single_evidence():

    accumulator = EvidenceAccumulator()

    updated = accumulator.record(
        make_artifact()
    )

    assert updated.evidence_count == 1


def test_adds_multiple_evidence():

    accumulator = EvidenceAccumulator()

    updated = accumulator.record(
        make_artifact(),
        amount=3,
    )

    assert updated.evidence_count == 3


def test_original_artifact_is_immutable():

    accumulator = EvidenceAccumulator()

    artifact = make_artifact()

    updated = accumulator.record(
        artifact
    )

    assert artifact.evidence_count == 0

    assert updated.evidence_count == 1


def test_invalid_amount():

    accumulator = EvidenceAccumulator()

    with pytest.raises(ValueError):

        accumulator.record(
            make_artifact(),
            amount=0,
        )
