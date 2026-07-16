from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.knowledge_runtime import (
    KnowledgeRuntime,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


def make_observation():

    return KnowledgeArtifact(
        identifier="OBS-001",
        title="Determinism",
        state=KnowledgeState.OBSERVATION,
    )


def test_runtime_is_functionally_deterministic():

    runtime = KnowledgeRuntime()

    first = runtime.record_observation(
        make_observation(),
        event_id="EVT-001",
    )

    second = runtime.record_observation(
        make_observation(),
        event_id="EVT-001",
    )

    #
    # Transition
    #

    assert (
        first.transition_executed
        ==
        second.transition_executed
    )

    #
    # Artifact
    #

    assert (
        first.artifact.state
        ==
        second.artifact.state
    )

    assert (
        first.artifact.evidence_count
        ==
        second.artifact.evidence_count
    )

    #
    # Runtime Event
    #

    assert (
        first.event.event_id
        ==
        second.event.event_id
    )

    assert (
        first.event.artifact_id
        ==
        second.event.artifact_id
    )

    assert (
        first.event.from_state
        ==
        second.event.from_state
    )

    assert (
        first.event.to_state
        ==
        second.event.to_state
    )

    #
    # Verification input
    #

    assert (
        first.event.evaluation
        ==
        second.event.evaluation
    )
