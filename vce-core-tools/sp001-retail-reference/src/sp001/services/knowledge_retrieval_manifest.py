from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidateSet,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
    KnowledgeRetrievalManifest,
)
from sp001.services.knowledge_source_retrieval import (
    evaluate_knowledge_source_retrieval,
)


def evaluate_knowledge_retrieval_candidates(
    *,
    candidate_set: KnowledgeRetrievalCandidateSet,
) -> KnowledgeRetrievalManifest:
    """Evaluate every candidate once while preserving declared order."""

    if not isinstance(
        candidate_set,
        KnowledgeRetrievalCandidateSet,
    ):
        raise TypeError(
            "candidate_set must be a "
            "KnowledgeRetrievalCandidateSet"
        )

    records = tuple(
        KnowledgeRetrievalCandidateDecision(
            candidate_id=candidate.candidate_id,
            decision=evaluate_knowledge_source_retrieval(
                source_status=candidate.source_status,
                content=candidate.content,
                effective_period=candidate.effective_period,
                retrieval_context=(
                    candidate_set.retrieval_context
                ),
                authority_bindings=(
                    candidate.authority_bindings
                ),
                supersession_graph=(
                    candidate_set.supersession_graph
                ),
            ),
        )
        for candidate in candidate_set.candidates
    )

    return KnowledgeRetrievalManifest(
        retrieval_context=candidate_set.retrieval_context,
        candidate_decisions=records,
    )
