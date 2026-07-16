from dataclasses import dataclass

from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)
from has.runtime.runtime_event import (
    RuntimeEvent,
)


@dataclass(frozen=True, slots=True)
class RuntimeResult:
    """Result of executing a runtime operation."""

    artifact: KnowledgeArtifact

    transition_executed: bool

    event: RuntimeEvent | None = None
