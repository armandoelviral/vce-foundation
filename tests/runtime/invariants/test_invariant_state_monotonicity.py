from has.runtime.knowledge_state import KnowledgeState
from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)


def test_state_graph_is_monotonic():

    policy = KnowledgeTransitionPolicy()

    states = (
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
        KnowledgeState.PRINCIPLE,
    )

    for destination in states:

        assert (
            policy.is_allowed(
                KnowledgeState.PRINCIPLE,
                destination,
            )
            is False
        )

    assert (
        policy.is_allowed(
            KnowledgeState.HYPOTHESIS,
            KnowledgeState.OBSERVATION,
        )
        is False
    )

    assert (
        policy.is_allowed(
            KnowledgeState.CANDIDATE_PRINCIPLE,
            KnowledgeState.HYPOTHESIS,
        )
        is False
    )
