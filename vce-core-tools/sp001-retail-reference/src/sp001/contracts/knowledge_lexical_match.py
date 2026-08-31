from dataclasses import dataclass
from enum import StrEnum

from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)


class KnowledgeLexicalMatchStatus(StrEnum):
    """Aggregate lexical presence without relevance claims."""

    ALL_TERMS_PRESENT = "ALL_TERMS_PRESENT"
    SOME_TERMS_PRESENT = "SOME_TERMS_PRESENT"
    NO_TERMS_PRESENT = "NO_TERMS_PRESENT"


@dataclass(frozen=True, slots=True)
class KnowledgeLexicalTermEvidence:
    """Exact occurrence evidence for one query-term position."""

    query_term_index: int
    term: str
    occurrence_count: int

    def __post_init__(self) -> None:
        if (
            isinstance(
                self.query_term_index,
                bool,
            )
            or not isinstance(
                self.query_term_index,
                int,
            )
        ):
            raise TypeError(
                "query_term_index must be an integer"
            )
        if self.query_term_index < 0:
            raise ValueError(
                "query_term_index must not be negative"
            )
        if (
            not isinstance(
                self.term,
                str,
            )
            or not self.term
        ):
            raise ValueError(
                "term must not be empty"
            )
        if (
            isinstance(
                self.occurrence_count,
                bool,
            )
            or not isinstance(
                self.occurrence_count,
                int,
            )
        ):
            raise TypeError(
                "occurrence_count must be an integer"
            )
        if self.occurrence_count < 0:
            raise ValueError(
                "occurrence_count must not be negative"
            )

    @property
    def is_present(self) -> bool:
        return self.occurrence_count > 0


@dataclass(frozen=True, slots=True)
class KnowledgeCandidateLexicalMatch:
    """Ordered lexical evidence for one technically included candidate."""

    query: KnowledgeLexicalQuery
    candidate_id: str
    source_identity: KnowledgeSourceIdentity
    term_evidence: tuple[
        KnowledgeLexicalTermEvidence,
        ...,
    ]
    match_status: KnowledgeLexicalMatchStatus

    def __post_init__(self) -> None:
        if not isinstance(
            self.query,
            KnowledgeLexicalQuery,
        ):
            raise TypeError(
                "query must be a KnowledgeLexicalQuery"
            )
        if (
            not isinstance(
                self.candidate_id,
                str,
            )
            or not self.candidate_id.strip()
        ):
            raise ValueError(
                "candidate_id must not be empty"
            )
        if not isinstance(
            self.source_identity,
            KnowledgeSourceIdentity,
        ):
            raise TypeError(
                "source_identity must be a "
                "KnowledgeSourceIdentity"
            )
        if not isinstance(
            self.term_evidence,
            tuple,
        ):
            raise TypeError(
                "term_evidence must be an immutable tuple"
            )
        if len(
            self.term_evidence
        ) != len(
            self.query.terms
        ):
            raise ValueError(
                "term_evidence must describe every query term"
            )

        for expected_index, evidence in enumerate(
            self.term_evidence
        ):
            if not isinstance(
                evidence,
                KnowledgeLexicalTermEvidence,
            ):
                raise TypeError(
                    "term_evidence must contain "
                    "KnowledgeLexicalTermEvidence values"
                )
            if evidence.query_term_index != expected_index:
                raise ValueError(
                    "term_evidence must preserve query-term order"
                )
            if evidence.term != self.query.terms[
                expected_index
            ]:
                raise ValueError(
                    "term_evidence must describe query terms"
                )

        if not isinstance(
            self.match_status,
            KnowledgeLexicalMatchStatus,
        ):
            raise TypeError(
                "match_status must be a "
                "KnowledgeLexicalMatchStatus"
            )

        present_count = sum(
            evidence.is_present
            for evidence in self.term_evidence
        )

        expected_status = (
            KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
            if present_count == len(
                self.term_evidence
            )
            else (
                KnowledgeLexicalMatchStatus.SOME_TERMS_PRESENT
                if present_count
                else KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
            )
        )

        if self.match_status is not expected_status:
            raise ValueError(
                "match_status must reflect term evidence"
            )
