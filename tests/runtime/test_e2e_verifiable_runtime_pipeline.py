from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_runtime import KnowledgeRuntime
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.runtime_event_verifier import (
    RuntimeEventVerifier,
)


def test_runtime_produces_verifiable_event():

    runtime = KnowledgeRuntime()

    verifier = RuntimeEventVerifier()

    artifact = KnowledgeArtifact(
        identifier="OBS-001",
        title="Verification",
        state=KnowledgeState.OBSERVATION,
    )

    result = runtime.record_observation(
        artifact,
        event_id="EVT-001",
    )

    assert result.transition_executed

    assert result.event is not None

    verification = verifier.verify(
        result.event,
    )

    assert verification.valid

    assert verification.reasons == ()
