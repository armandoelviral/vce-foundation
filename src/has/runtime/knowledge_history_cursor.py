from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


class KnowledgeHistoryCursor:
    """Sequential navigation over immutable history."""

    def __init__(
        self,
        history: KnowledgeHistory,
    ) -> None:
        self._history = history
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(
            self._history.events
        )

    def next(
        self,
    ) -> RuntimeEvent:

        event = self._history.events[
            self._index
        ]

        self._index += 1

        return event

    def reset(
        self,
    ) -> None:

        self._index = 0
