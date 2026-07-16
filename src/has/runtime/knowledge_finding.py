from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeFinding:
    """Result of inspecting knowledge history."""

    code: str

    message: str

    severity: str
