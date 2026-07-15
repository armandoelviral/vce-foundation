from dataclasses import dataclass

from has.runtime.knowledge_state import KnowledgeState


@dataclass(frozen=True)
class KnowledgeArtifact:

    identifier: str

    title: str

    state: KnowledgeState

    evidence_count: int = 0

    destruction_attempts: int = 0

    independent_validations: int = 0
