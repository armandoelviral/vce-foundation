from has.runtime.knowledge_state import (
    KnowledgeState,
)

from has.runtime.knowledge_state_order import (
    STATE_ORDER,
)


def test_states_are_ordered():

    assert (
        STATE_ORDER[
            KnowledgeState.OBSERVATION
        ]
        <
        STATE_ORDER[
            KnowledgeState.HYPOTHESIS
        ]
    )

    assert (
        STATE_ORDER[
            KnowledgeState.HYPOTHESIS
        ]
        <
        STATE_ORDER[
            KnowledgeState.CANDIDATE_PRINCIPLE
        ]
    )

    assert (
        STATE_ORDER[
            KnowledgeState.CANDIDATE_PRINCIPLE
        ]
        <
        STATE_ORDER[
            KnowledgeState.PRINCIPLE
        ]
    )
