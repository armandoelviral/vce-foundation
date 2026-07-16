from collections.abc import Mapping
from dataclasses import dataclass
from dataclasses import field

from has.runtime.knowledge_state import KnowledgeState


@dataclass(frozen=True, slots=True)
class KnowledgeArtifact:
    identifier: str
    title: str
    state: KnowledgeState
    evidence_count: int = 0
    destruction_attempts: int = 0
    independent_validations: int = 0
    metadata: Mapping[str, object] = field(
        default_factory=dict,
    )
