from dataclasses import dataclass

from sp001.contracts.knowledge_lexical_ordering import (
    KnowledgeLexicalOrdering,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
    KnowledgeRetrievalManifest,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalResult:
    """Complete governance disposition plus ordered lexical evidence."""

    query: KnowledgeLexicalQuery
    manifest: KnowledgeRetrievalManifest
    lexical_ordering: KnowledgeLexicalOrdering

    def __post_init__(self) -> None:
        if not isinstance(
            self.query,
            KnowledgeLexicalQuery,
        ):
            raise TypeError(
                "query must be a KnowledgeLexicalQuery"
            )
        if not isinstance(
            self.manifest,
            KnowledgeRetrievalManifest,
        ):
            raise TypeError(
                "manifest must be a KnowledgeRetrievalManifest"
            )
        if not isinstance(
            self.lexical_ordering,
            KnowledgeLexicalOrdering,
        ):
            raise TypeError(
                "lexical_ordering must be a "
                "KnowledgeLexicalOrdering"
            )
        if self.lexical_ordering.query != self.query:
            raise ValueError(
                "lexical_ordering must use result query"
            )

        included_records = tuple(
            record
            for record in self.manifest.candidate_decisions
            if (
                record.decision.decision_status
                is KnowledgeRetrievalDecisionStatus.INCLUDED
            )
        )
        included_by_candidate_id = {
            record.candidate_id: record
            for record in included_records
        }
        ordered_candidate_ids = tuple(
            entry.evidence.match.candidate_id
            for entry in self.lexical_ordering.entries
        )

        if set(
            ordered_candidate_ids
        ) != set(
            included_by_candidate_id
        ):
            raise ValueError(
                "lexical_ordering must contain every and only "
                "included manifest candidate"
            )
        if len(
            ordered_candidate_ids
        ) != len(
            included_records
        ):
            raise ValueError(
                "lexical_ordering must contain each included "
                "manifest candidate exactly once"
            )

        for entry in self.lexical_ordering.entries:
            match = entry.evidence.match
            record = included_by_candidate_id[
                match.candidate_id
            ]
            if (
                match.source_identity
                != record.decision.source_status.identity
            ):
                raise ValueError(
                    "lexical evidence source must match "
                    "manifest decision source"
                )

    @property
    def included_candidate_decisions(
        self,
    ) -> tuple[
        KnowledgeRetrievalCandidateDecision,
        ...,
    ]:
        return tuple(
            record
            for record in self.manifest.candidate_decisions
            if (
                record.decision.decision_status
                is KnowledgeRetrievalDecisionStatus.INCLUDED
            )
        )

    @property
    def excluded_candidate_decisions(
        self,
    ) -> tuple[
        KnowledgeRetrievalCandidateDecision,
        ...,
    ]:
        return tuple(
            record
            for record in self.manifest.candidate_decisions
            if (
                record.decision.decision_status
                is KnowledgeRetrievalDecisionStatus.EXCLUDED
            )
        )

    @property
    def ordered_candidate_ids(
        self,
    ) -> tuple[str, ...]:
        return tuple(
            entry.evidence.match.candidate_id
            for entry in self.lexical_ordering.entries
        )
