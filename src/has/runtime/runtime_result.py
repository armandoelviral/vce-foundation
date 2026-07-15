from dataclasses import dataclass

from has.runtime.knowledge_artifact import (
    KnowledgeArtifact,
)


@dataclass(frozen=True, slots=True)
class RuntimeResult:

    artifact: KnowledgeArtifact

    transition_executed: bool
