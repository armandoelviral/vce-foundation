from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
    KnowledgeLexicalTermEvidence,
)
from sp001.contracts.knowledge_lexical_ordering import (
    KnowledgeLexicalOrdering,
    KnowledgeLexicalOrderingEntry,
)
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KnowledgeCandidateLexicalOrderingEvidence,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_lexical_query,
)


def project_knowledge_lexical_ordering(
    *,
    ordering: KnowledgeLexicalOrdering,
) -> dict[str, object]:
    """Project validated lexical ordering without reevaluation."""

    if not isinstance(
        ordering,
        KnowledgeLexicalOrdering,
    ):
        raise TypeError(
            "ordering must be a KnowledgeLexicalOrdering"
        )

    return {
        "query": project_knowledge_lexical_query(
            query=ordering.query,
        ),
        "entries": [
            _ordering_entry_document(entry)
            for entry in ordering.entries
        ],
        "ordering_policy": ordering.ordering_policy,
    }


def _ordering_entry_document(
    entry: KnowledgeLexicalOrderingEntry,
) -> dict[str, object]:
    return {
        "declared_candidate_index": (
            entry.declared_candidate_index
        ),
        "ordered_candidate_index": (
            entry.ordered_candidate_index
        ),
        "evidence": _ordering_evidence_document(
            entry.evidence
        ),
    }


def _ordering_evidence_document(
    evidence: KnowledgeCandidateLexicalOrderingEvidence,
) -> dict[str, object]:
    return {
        "match": _match_document(
            evidence.match
        ),
        "status_precedence": evidence.status_precedence,
        "present_query_term_count": (
            evidence.present_query_term_count
        ),
        "total_occurrence_count": (
            evidence.total_occurrence_count
        ),
        "ordering_key": list(
            evidence.ordering_key
        ),
        "ordering_policy": evidence.ordering_policy,
    }


def _match_document(
    match: KnowledgeCandidateLexicalMatch,
) -> dict[str, object]:
    return {
        "query": project_knowledge_lexical_query(
            query=match.query,
        ),
        "candidate_id": match.candidate_id,
        "source_identity": _source_identity_document(
            match.source_identity
        ),
        "term_evidence": [
            _term_evidence_document(term)
            for term in match.term_evidence
        ],
        "match_status": match.match_status.value,
    }


def _source_identity_document(
    identity: KnowledgeSourceIdentity,
) -> dict[str, object]:
    return {
        "source_id": identity.source_id,
        "source_version": identity.source_version,
        "source_content_digest": {
            "algorithm": (
                identity.source_content_digest.algorithm
            ),
            "value": identity.source_content_digest.value,
        },
    }


def _term_evidence_document(
    evidence: KnowledgeLexicalTermEvidence,
) -> dict[str, object]:
    return {
        "query_term_index": evidence.query_term_index,
        "term": evidence.term,
        "occurrence_count": evidence.occurrence_count,
    }
