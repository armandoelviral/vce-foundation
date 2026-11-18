from dataclasses import dataclass

from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityBinding,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)


@dataclass(frozen=True, slots=True)
class Product001DocumentaryInputs:
    """Inputs for independent SP001 retrieval evaluation.

    This value does not confer authority.
    """

    source_status: KnowledgeSourceStatus
    content: bytes
    effective_period: KnowledgeSourceEffectivePeriod
    retrieval_context: KnowledgeRetrievalContext
    authority_bindings: tuple[KnowledgeAuthorityBinding, ...]
    supersession_graph: KnowledgeSourceSupersessionGraph

    def __post_init__(self) -> None:
        if not isinstance(
            self.source_status, KnowledgeSourceStatus
        ):
            raise TypeError("invalid source_status")

        if type(self.content) is not bytes:
            raise TypeError("content must be bytes")

        if not isinstance(
            self.effective_period,
            KnowledgeSourceEffectivePeriod,
        ):
            raise TypeError("invalid effective_period")

        if not isinstance(
            self.retrieval_context,
            KnowledgeRetrievalContext,
        ):
            raise TypeError("invalid retrieval_context")

        if type(self.authority_bindings) is not tuple:
            raise TypeError("authority_bindings must be tuple")

        if not all(
            isinstance(item, KnowledgeAuthorityBinding)
            for item in self.authority_bindings
        ):
            raise TypeError("invalid authority binding")

        if not isinstance(
            self.supersession_graph,
            KnowledgeSourceSupersessionGraph,
        ):
            raise TypeError("invalid supersession_graph")
