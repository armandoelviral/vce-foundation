from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


class KnowledgeHistoryQuery:
    """Read-only queries over immutable knowledge history."""

    def latest(
        self,
        history: KnowledgeHistory,
    ) -> RuntimeEvent | None:

        if not history.events:
            return None

        return history.events[-1]

    def by_artifact(
        self,
        history: KnowledgeHistory,
        artifact_id: str,
    ) -> tuple[RuntimeEvent, ...]:

        return tuple(
            event
            for event in history.events
            if event.artifact_id == artifact_id
        )

    def count(
        self,
        history: KnowledgeHistory,
    ) -> int:

        return len(history)
