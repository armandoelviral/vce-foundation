from collections import Counter

from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
    KnowledgeLexicalMatchStatus,
    KnowledgeLexicalTermEvidence,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidate,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
)
from sp001.services.knowledge_lexical_text_normalization import (
    normalize_knowledge_lexical_text,
)


def evaluate_knowledge_candidate_lexical_match(
    *,
    query: KnowledgeLexicalQuery,
    candidate: KnowledgeRetrievalCandidate,
    candidate_decision: KnowledgeRetrievalCandidateDecision,
) -> KnowledgeCandidateLexicalMatch:
    """Count complete normalized terms for one included candidate."""

    if not isinstance(
        query,
        KnowledgeLexicalQuery,
    ):
        raise TypeError(
            "query must be a KnowledgeLexicalQuery"
        )
    if not isinstance(
        candidate,
        KnowledgeRetrievalCandidate,
    ):
        raise TypeError(
            "candidate must be a KnowledgeRetrievalCandidate"
        )
    if not isinstance(
        candidate_decision,
        KnowledgeRetrievalCandidateDecision,
    ):
        raise TypeError(
            "candidate_decision must be a "
            "KnowledgeRetrievalCandidateDecision"
        )
    if candidate_decision.candidate_id != candidate.candidate_id:
        raise ValueError(
            "candidate_decision must describe candidate_id"
        )
    if (
        candidate_decision.decision.source_status
        != candidate.source_status
    ):
        raise ValueError(
            "candidate_decision must describe candidate source"
        )
    if (
        candidate_decision.decision.decision_status
        is not KnowledgeRetrievalDecisionStatus.INCLUDED
    ):
        raise ValueError(
            "lexical matching requires an INCLUDED decision"
        )
    if (
        candidate_decision.decision.content_bytes_match_digest
        is not True
    ):
        raise ValueError(
            "included decision must verify candidate content bytes"
        )

    content_text = candidate.content.decode(
        "UTF-8",
        errors="strict",
    )
    normalized_content = normalize_knowledge_lexical_text(
        text=content_text,
    )
    content_terms = (
        tuple(
            normalized_content.split(" ")
        )
        if normalized_content
        else ()
    )
    occurrences = Counter(
        content_terms
    )

    term_evidence = tuple(
        KnowledgeLexicalTermEvidence(
            query_term_index=index,
            term=term,
            occurrence_count=occurrences[
                term
            ],
        )
        for index, term in enumerate(
            query.terms
        )
    )

    present_count = sum(
        evidence.is_present
        for evidence in term_evidence
    )
    match_status = (
        KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
        if present_count == len(
            term_evidence
        )
        else (
            KnowledgeLexicalMatchStatus.SOME_TERMS_PRESENT
            if present_count
            else KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
        )
    )

    return KnowledgeCandidateLexicalMatch(
        query=query,
        candidate_id=candidate.candidate_id,
        source_identity=candidate.source_status.identity,
        term_evidence=term_evidence,
        match_status=match_status,
    )
