from has.runtime.knowledge_history import KnowledgeHistory
from has.runtime.runtime_event_verifier import RuntimeEventVerifier
from has.runtime.runtime_result import RuntimeResult


class KnowledgeHistoryRecorder:
    """Records only verified runtime events into immutable history."""

    def __init__(
        self,
        verifier: RuntimeEventVerifier | None = None,
    ) -> None:
        self._verifier = (
            verifier
            if verifier is not None
            else RuntimeEventVerifier()
        )

    def record(
        self,
        history: KnowledgeHistory,
        result: RuntimeResult,
    ) -> KnowledgeHistory:
        if result.event is None:
            return history

        verification = self._verifier.verify(
            result.event,
        )

        if not verification.valid:
            reasons = ", ".join(
                verification.reasons,
            )

            raise ValueError(
                "runtime event verification failed: "
                f"{reasons}"
            )

        return history.append(
            result.event,
        )
