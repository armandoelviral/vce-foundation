from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_promoter import (
    KnowledgePromoter,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def make_observation():

    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
    )


def test_promotes_to_hypothesis():

    promoter = KnowledgePromoter()

    updated = promoter.promote(
        make_observation(),
        KnowledgeState.HYPOTHESIS,
    )

    assert (
        updated.state
        is KnowledgeState.HYPOTHESIS
    )


def test_original_object_is_not_modified():

    promoter = KnowledgePromoter()

    artifact = make_observation()

    updated = promoter.promote(
        artifact,
        KnowledgeState.HYPOTHESIS,
    )

    assert (
        artifact.state
        is KnowledgeState.OBSERVATION
    )

    assert (
        updated.state
        is KnowledgeState.HYPOTHESIS
    )
