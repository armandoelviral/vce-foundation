from sp001.contracts.knowledge_lexical_ordering import (
    KnowledgeLexicalOrdering,
    KnowledgeLexicalOrderingEntry,
)
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KnowledgeCandidateLexicalOrderingEvidence,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)


def order_knowledge_candidate_lexical_evidence(
    *,
    query: KnowledgeLexicalQuery,
    evidence: tuple[
        KnowledgeCandidateLexicalOrderingEvidence,
        ...,
    ],
) -> KnowledgeLexicalOrdering:
    """Order lexical evidence while preserving declared ties."""

    if not isinstance(
        query,
        KnowledgeLexicalQuery,
    ):
        raise TypeError(
            "query must be a KnowledgeLexicalQuery"
        )
    if not isinstance(
        evidence,
        tuple,
    ):
        raise TypeError(
            "evidence must be an immutable tuple"
        )

    indexed_evidence: list[
        tuple[
            int,
            KnowledgeCandidateLexicalOrderingEvidence,
        ]
    ] = []

    for declared_index, candidate_evidence in enumerate(
        evidence
    ):
        if not isinstance(
            candidate_evidence,
            KnowledgeCandidateLexicalOrderingEvidence,
        ):
            raise TypeError(
                "evidence must contain "
                "KnowledgeCandidateLexicalOrderingEvidence values"
            )
        if candidate_evidence.match.query != query:
            raise ValueError(
                "candidate evidence must use ordering query"
            )

        indexed_evidence.append(
            (
                declared_index,
                candidate_evidence,
            )
        )

    ordered = sorted(
        indexed_evidence,
        key=lambda item: (
            -item[1].status_precedence,
            -item[1].present_query_term_count,
            -item[1].total_occurrence_count,
            item[0],
        ),
    )

    entries = tuple(
        KnowledgeLexicalOrderingEntry(
            declared_candidate_index=declared_index,
            ordered_candidate_index=ordered_index,
            evidence=candidate_evidence,
        )
        for ordered_index, (
            declared_index,
            candidate_evidence,
        ) in enumerate(
            ordered
        )
    )

    return KnowledgeLexicalOrdering(
        query=query,
        entries=entries,
    )
