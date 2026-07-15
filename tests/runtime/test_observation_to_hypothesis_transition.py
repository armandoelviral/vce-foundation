from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.transitions.observation_to_hypothesis_transition import (
    ObservationToHypothesisTransition,
)


def test_observation_becomes_hypothesis():

    transition = (
        ObservationToHypothesisTransition()
    )

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Example",
        state=KnowledgeState.OBSERVATION,
    )

    updated = transition.execute(
        artifact
    )

    assert (
        updated.state
        is KnowledgeState.HYPOTHESIS
    )

    assert updated.evidence_count == 1
