from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeState:

    event_count: int
    last_sequence: int
