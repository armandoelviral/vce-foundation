from dataclasses import dataclass

from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityBinding,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalCandidate:
    """Immutable source material required for one retrieval evaluation."""

    candidate_id: str
    source_status: KnowledgeSourceStatus
    content: bytes
    effective_period: KnowledgeSourceEffectivePeriod
    authority_bindings: tuple[
        KnowledgeAuthorityBinding,
        ...,
    ]

    def __post_init__(self) -> None:
        if (
            not isinstance(self.candidate_id, str)
            or not self.candidate_id.strip()
        ):
            raise ValueError(
                "candidate_id must not be empty"
            )

        if not isinstance(
            self.source_status,
            KnowledgeSourceStatus,
        ):
            raise TypeError(
                "source_status must be a KnowledgeSourceStatus"
            )

        if not isinstance(self.content, bytes):
            raise TypeError(
                "content must be immutable bytes"
            )

        if not self.content:
            raise ValueError(
                "content must not be empty"
            )

        if not isinstance(
            self.effective_period,
            KnowledgeSourceEffectivePeriod,
        ):
            raise TypeError(
                "effective_period must be a "
                "KnowledgeSourceEffectivePeriod"
            )

        if (
            self.effective_period.source_status
            != self.source_status
        ):
            raise ValueError(
                "effective_period must describe source_status"
            )

        if not isinstance(self.authority_bindings, tuple):
            raise TypeError(
                "authority_bindings must be an immutable tuple"
            )

        seen_binding_ids: set[str] = set()

        for binding in self.authority_bindings:
            if not isinstance(
                binding,
                KnowledgeAuthorityBinding,
            ):
                raise TypeError(
                    "authority_bindings must contain "
                    "KnowledgeAuthorityBinding values"
                )

            if (
                binding.authority_binding_id
                in seen_binding_ids
            ):
                raise ValueError(
                    "duplicate authority_binding_id: "
                    f"{binding.authority_binding_id}"
                )

            seen_binding_ids.add(
                binding.authority_binding_id,
            )


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalCandidateSet:
    """Ordered evaluation input preserving the complete candidate universe."""

    retrieval_context: KnowledgeRetrievalContext
    candidates: tuple[
        KnowledgeRetrievalCandidate,
        ...,
    ]
    supersession_graph: KnowledgeSourceSupersessionGraph

    def __post_init__(self) -> None:
        if not isinstance(
            self.retrieval_context,
            KnowledgeRetrievalContext,
        ):
            raise TypeError(
                "retrieval_context must be a "
                "KnowledgeRetrievalContext"
            )

        if not isinstance(self.candidates, tuple):
            raise TypeError(
                "candidates must be an immutable tuple"
            )

        seen_candidate_ids: set[str] = set()
        seen_source_identities: set[object] = set()

        for candidate in self.candidates:
            if not isinstance(
                candidate,
                KnowledgeRetrievalCandidate,
            ):
                raise TypeError(
                    "candidates must contain "
                    "KnowledgeRetrievalCandidate values"
                )

            if candidate.candidate_id in seen_candidate_ids:
                raise ValueError(
                    "duplicate candidate_id: "
                    f"{candidate.candidate_id}"
                )

            seen_candidate_ids.add(
                candidate.candidate_id,
            )

            source_identity = candidate.source_status.identity

            if source_identity in seen_source_identities:
                raise ValueError(
                    "duplicate candidate source identity: "
                    f"{source_identity.source_id} "
                    f"{source_identity.source_version}"
                )

            seen_source_identities.add(
                source_identity,
            )

        if not isinstance(
            self.supersession_graph,
            KnowledgeSourceSupersessionGraph,
        ):
            raise TypeError(
                "supersession_graph must be a "
                "KnowledgeSourceSupersessionGraph"
            )
