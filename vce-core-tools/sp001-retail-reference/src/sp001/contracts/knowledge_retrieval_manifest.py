from dataclasses import dataclass

from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeSourceRetrievalDecision,
)


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalCandidateDecision:
    """One candidate identity bound to its complete technical decision."""

    candidate_id: str
    decision: KnowledgeSourceRetrievalDecision

    def __post_init__(self) -> None:
        if (
            not isinstance(self.candidate_id, str)
            or not self.candidate_id.strip()
        ):
            raise ValueError(
                "candidate_id must not be empty"
            )

        if not isinstance(
            self.decision,
            KnowledgeSourceRetrievalDecision,
        ):
            raise TypeError(
                "decision must be a "
                "KnowledgeSourceRetrievalDecision"
            )


@dataclass(frozen=True, slots=True)
class KnowledgeRetrievalManifest:
    """Complete ordered disposition of one candidate universe."""

    retrieval_context: KnowledgeRetrievalContext
    candidate_decisions: tuple[
        KnowledgeRetrievalCandidateDecision,
        ...,
    ]

    def __post_init__(self) -> None:
        if not isinstance(
            self.retrieval_context,
            KnowledgeRetrievalContext,
        ):
            raise TypeError(
                "retrieval_context must be a "
                "KnowledgeRetrievalContext"
            )

        if not isinstance(
            self.candidate_decisions,
            tuple,
        ):
            raise TypeError(
                "candidate_decisions must be an immutable tuple"
            )

        seen_candidate_ids: set[str] = set()
        seen_source_identities: set[object] = set()

        for record in self.candidate_decisions:
            if not isinstance(
                record,
                KnowledgeRetrievalCandidateDecision,
            ):
                raise TypeError(
                    "candidate_decisions must contain "
                    "KnowledgeRetrievalCandidateDecision values"
                )

            if record.candidate_id in seen_candidate_ids:
                raise ValueError(
                    "duplicate candidate_id: "
                    f"{record.candidate_id}"
                )

            seen_candidate_ids.add(record.candidate_id)

            if (
                record.decision.retrieval_context
                != self.retrieval_context
            ):
                raise ValueError(
                    "candidate decision must use "
                    "manifest retrieval context"
                )

            source_identity = (
                record.decision.source_status.identity
            )

            if source_identity in seen_source_identities:
                raise ValueError(
                    "duplicate decision source identity: "
                    f"{source_identity.source_id} "
                    f"{source_identity.source_version}"
                )

            seen_source_identities.add(source_identity)

    @property
    def all_decisions(
        self,
    ) -> tuple[KnowledgeSourceRetrievalDecision, ...]:
        return tuple(
            record.decision
            for record in self.candidate_decisions
        )

    @property
    def included_decisions(
        self,
    ) -> tuple[KnowledgeSourceRetrievalDecision, ...]:
        return tuple(
            record.decision
            for record in self.candidate_decisions
            if (
                record.decision.decision_status
                is KnowledgeRetrievalDecisionStatus.INCLUDED
            )
        )

    @property
    def excluded_decisions(
        self,
    ) -> tuple[KnowledgeSourceRetrievalDecision, ...]:
        return tuple(
            record.decision
            for record in self.candidate_decisions
            if (
                record.decision.decision_status
                is KnowledgeRetrievalDecisionStatus.EXCLUDED
            )
        )
