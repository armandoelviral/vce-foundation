from dataclasses import dataclass

from has.runtime.evaluation_result import (
    EvaluationResult,
)
from has.runtime.knowledge_state import (
    KnowledgeState,
)


@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    """Immutable description of a runtime transition."""

    artifact_id: str

    from_state: KnowledgeState

    to_state: KnowledgeState

    evaluation: EvaluationResult
