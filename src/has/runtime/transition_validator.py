from has.runtime.knowledge_state import (
    KnowledgeState,
)

from has.runtime.knowledge_state_order import (
    STATE_ORDER,
)


class TransitionValidator:

    def can_transition(
        self,
        from_state: KnowledgeState,
        to_state: KnowledgeState,
    ) -> bool:

        return (
            STATE_ORDER[to_state]
            >
            STATE_ORDER[from_state]
        )
