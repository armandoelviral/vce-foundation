from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.knowledge_replay import (
    KnowledgeReplay,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


def make_history() -> KnowledgeHistory:

    return (
        KnowledgeHistory()

        .append(
            RuntimeEvent(
                event_id="EVT-001",
                artifact_id="K-001",
                from_state=KnowledgeState.OBSERVATION,
                to_state=KnowledgeState.HYPOTHESIS,
                evaluation=EvaluationResult(
                    eligible=True,
                ),
            )
        )

        .append(
            RuntimeEvent(
                event_id="EVT-002",
                artifact_id="K-001",
                from_state=KnowledgeState.HYPOTHESIS,
                to_state=KnowledgeState.CANDIDATE_PRINCIPLE,
                evaluation=EvaluationResult(
                    eligible=True,
                ),
            )
        )

        .append(
            RuntimeEvent(
                event_id="EVT-003",
                artifact_id="K-001",
                from_state=KnowledgeState.CANDIDATE_PRINCIPLE,
                to_state=KnowledgeState.PRINCIPLE,
                evaluation=EvaluationResult(
                    eligible=True,
                ),
            )
        )
    )


def test_replay_is_deterministic():

    history = make_history()

    replay = KnowledgeReplay()

    first = replay.replay(
        history,
        "K-001",
    )

    second = replay.replay(
        history,
        "K-001",
    )

    third = replay.replay(
        history,
        "K-001",
    )

    assert first == second == third


def test_multiple_replay_instances_are_identical():

    history = make_history()

    first = (
        KnowledgeReplay()
        .replay(
            history,
            "K-001",
        )
    )

    second = (
        KnowledgeReplay()
        .replay(
            history,
            "K-001",
        )
    )

    assert first == second


def test_replay_does_not_modify_history():

    history = make_history()

    before = history.events

    KnowledgeReplay().replay(
        history,
        "K-001",
    )

    after = history.events

    assert before == after
