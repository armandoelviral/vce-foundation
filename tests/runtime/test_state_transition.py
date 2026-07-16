from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.state_transition import StateTransition


def make_observation() -> KnowledgeArtifact:
    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Observation",
        state=KnowledgeState.OBSERVATION,
    )


def test_applies_target_state() -> None:
    transition = StateTransition()

    updated = transition.apply(
        make_observation(),
        KnowledgeState.HYPOTHESIS,
    )

    assert updated.state is KnowledgeState.HYPOTHESIS


def test_does_not_mutate_original_artifact() -> None:
    transition = StateTransition()
    artifact = make_observation()

    updated = transition.apply(
        artifact,
        KnowledgeState.HYPOTHESIS,
    )

    assert artifact.state is KnowledgeState.OBSERVATION
    assert updated.state is KnowledgeState.HYPOTHESIS
