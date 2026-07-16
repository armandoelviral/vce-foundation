from dataclasses import dataclass
from dataclasses import field

from has.runtime.knowledge_state import KnowledgeState


DEFAULT_ALLOWED_TRANSITIONS = frozenset({
    (
        KnowledgeState.OBSERVATION,
        KnowledgeState.HYPOTHESIS,
    ),
    (
        KnowledgeState.HYPOTHESIS,
        KnowledgeState.CANDIDATE_PRINCIPLE,
    ),
    (
        KnowledgeState.CANDIDATE_PRINCIPLE,
        KnowledgeState.PRINCIPLE,
    ),
})


@dataclass(frozen=True, slots=True)
class KnowledgeTransitionPolicy:
    """Defines the knowledge-state transitions permitted by the domain."""

    allowed_transitions: frozenset[
        tuple[KnowledgeState, KnowledgeState]
    ] = field(
        default_factory=lambda: DEFAULT_ALLOWED_TRANSITIONS,
    )

    def is_allowed(
        self,
        from_state: KnowledgeState,
        to_state: KnowledgeState,
    ) -> bool:
        return (
            from_state,
            to_state,
        ) in self.allowed_transitions
