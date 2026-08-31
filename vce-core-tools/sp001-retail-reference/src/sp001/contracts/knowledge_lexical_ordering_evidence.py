from dataclasses import dataclass, field

from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
    KnowledgeLexicalMatchStatus,
)


KNOWLEDGE_LEXICAL_ORDERING_POLICY = (
    "MATCH_STATUS_PRESENT_QUERY_TERMS_TOTAL_OCCURRENCES_V1"
)

_MATCH_STATUS_PRECEDENCE = {
    KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT: 2,
    KnowledgeLexicalMatchStatus.SOME_TERMS_PRESENT: 1,
    KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT: 0,
}


@dataclass(frozen=True, slots=True)
class KnowledgeCandidateLexicalOrderingEvidence:
    """Mechanical lexical ordering evidence without relevance claims."""

    match: KnowledgeCandidateLexicalMatch
    status_precedence: int = field(
        init=False,
    )
    present_query_term_count: int = field(
        init=False,
    )
    total_occurrence_count: int = field(
        init=False,
    )
    ordering_key: tuple[int, int, int] = field(
        init=False,
    )
    ordering_policy: str = field(
        init=False,
        default=KNOWLEDGE_LEXICAL_ORDERING_POLICY,
    )

    def __post_init__(self) -> None:
        if not isinstance(
            self.match,
            KnowledgeCandidateLexicalMatch,
        ):
            raise TypeError(
                "match must be a "
                "KnowledgeCandidateLexicalMatch"
            )

        status_precedence = _MATCH_STATUS_PRECEDENCE[
            self.match.match_status
        ]
        present_query_term_count = sum(
            evidence.is_present
            for evidence in self.match.term_evidence
        )
        total_occurrence_count = sum(
            evidence.occurrence_count
            for evidence in self.match.term_evidence
        )
        ordering_key = (
            status_precedence,
            present_query_term_count,
            total_occurrence_count,
        )

        object.__setattr__(
            self,
            "status_precedence",
            status_precedence,
        )
        object.__setattr__(
            self,
            "present_query_term_count",
            present_query_term_count,
        )
        object.__setattr__(
            self,
            "total_occurrence_count",
            total_occurrence_count,
        )
        object.__setattr__(
            self,
            "ordering_key",
            ordering_key,
        )
