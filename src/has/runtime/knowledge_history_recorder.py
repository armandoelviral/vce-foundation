from has.runtime.knowledge_history import (
    KnowledgeHistory,
)
from has.runtime.runtime_result import (
    RuntimeResult,
)


class KnowledgeHistoryRecorder:
    """Records runtime events into an immutable history."""

    def record(
        self,
        history: KnowledgeHistory,
        result: RuntimeResult,
    ) -> KnowledgeHistory:

        if result.event is None:
            return history

        return history.append(
            result.event,
        )
