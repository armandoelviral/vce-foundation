from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)
from has.runtime.runtime_event_verifier import (
    RuntimeEventVerifier,
)


def event(
    event_id,
    from_state,
    to_state,
):

    return RuntimeEvent(
        event_id=event_id,
        artifact_id="K-001",
        from_state=from_state,
        to_state=to_state,
        evaluation=EvaluationResult(
            eligible=True,
        ),
    )


def test_every_event_in_history_is_verifiable():

    history = (
        KnowledgeHistory()

        .append(
            event(
                "EVT-001",
                KnowledgeState.OBSERVATION,
                KnowledgeState.HYPOTHESIS,
            )
        )

        .append(
            event(
                "EVT-002",
                KnowledgeState.HYPOTHESIS,
                KnowledgeState.CANDIDATE_PRINCIPLE,
            )
        )

        .append(
            event(
                "EVT-003",
                KnowledgeState.CANDIDATE_PRINCIPLE,
                KnowledgeState.PRINCIPLE,
            )
        )
    )

    verifier = RuntimeEventVerifier()

    for runtime_event in history.events:

        verification = verifier.verify(
            runtime_event,
        )

        assert verification.valid
