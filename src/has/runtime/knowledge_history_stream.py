from collections.abc import Iterator

from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


class KnowledgeHistoryStream:
    """Read-only streaming access to immutable history."""

    def stream(
        self,
        history: KnowledgeHistory,
    ) -> Iterator[RuntimeEvent]:
        yield from history.events
