from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.knowledge_history_query import (
    KnowledgeHistoryQuery,
)
from has.runtime.knowledge_state import KnowledgeState


class KnowledgeReplay:
    """Reconstructs the latest known state of one artifact."""

    def __init__(
        self,
        query: KnowledgeHistoryQuery | None = None,
    ) -> None:
        self._query = query or KnowledgeHistoryQuery()

    def replay(
        self,
        history: KnowledgeHistory,
        artifact_id: str,
    ) -> KnowledgeState | None:
        events = self._query.by_artifact(
            history,
            artifact_id,
        )

        if not events:
            return None

        current_state = events[0].from_state

        for event in events:
            if event.from_state is not current_state:
                raise ValueError(
                    "discontinuous knowledge history for "
                    f"artifact: {artifact_id}"
                )

            current_state = event.to_state

        return current_state
