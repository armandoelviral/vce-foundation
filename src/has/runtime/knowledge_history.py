from dataclasses import dataclass

from has.runtime.runtime_event import RuntimeEvent


@dataclass(frozen=True, slots=True)
class KnowledgeHistory:
    """Immutable ordered history of runtime events."""

    events: tuple[RuntimeEvent, ...] = ()

    def append(
        self,
        event: RuntimeEvent,
    ) -> "KnowledgeHistory":
        if self.contains(event.event_id):
            raise ValueError(
                f"event_id already exists: {event.event_id}"
            )

        return KnowledgeHistory(
            events=(*self.events, event),
        )

    def contains(
        self,
        event_id: str,
    ) -> bool:
        return any(
            event.event_id == event_id
            for event in self.events
        )

    def __len__(self) -> int:
        return len(self.events)
