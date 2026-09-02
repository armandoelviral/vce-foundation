from sp001.contracts.knowledge_governed_retrieval import (
    KnowledgeGovernedRetrievalResult,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidateSet,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.services.knowledge_candidate_lexical_matching import (
    evaluate_knowledge_candidate_lexical_match,
)
from sp001.services.knowledge_lexical_ordering import (
    order_knowledge_candidate_lexical_evidence,
)
from sp001.services.knowledge_lexical_ordering_evidence import (
    materialize_knowledge_candidate_lexical_ordering_evidence,
)
from sp001.services.knowledge_retrieval_manifest import (
    evaluate_knowledge_retrieval_candidates,
)


def execute_governed_knowledge_retrieval(
    *,
    query: KnowledgeLexicalQuery,
    candidate_set: KnowledgeRetrievalCandidateSet,
) -> KnowledgeGovernedRetrievalResult:
    """Compose governance, lexical evidence and stable ordering."""

    if not isinstance(
        query,
        KnowledgeLexicalQuery,
    ):
        raise TypeError(
            "query must be a KnowledgeLexicalQuery"
        )
    if not isinstance(
        candidate_set,
        KnowledgeRetrievalCandidateSet,
    ):
        raise TypeError(
            "candidate_set must be a "
            "KnowledgeRetrievalCandidateSet"
        )

    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=candidate_set,
    )

    if len(
        manifest.candidate_decisions
    ) != len(
        candidate_set.candidates
    ):
        raise ValueError(
            "manifest must describe complete candidate set"
        )

    ordering_evidence = tuple(
        materialize_knowledge_candidate_lexical_ordering_evidence(
            match=evaluate_knowledge_candidate_lexical_match(
                query=query,
                candidate=candidate,
                candidate_decision=candidate_decision,
            ),
        )
        for candidate, candidate_decision in zip(
            candidate_set.candidates,
            manifest.candidate_decisions,
        )
        if (
            candidate_decision.decision.decision_status
            is KnowledgeRetrievalDecisionStatus.INCLUDED
        )
    )

    lexical_ordering = (
        order_knowledge_candidate_lexical_evidence(
            query=query,
            evidence=ordering_evidence,
        )
    )

    return KnowledgeGovernedRetrievalResult(
        query=query,
        manifest=manifest,
        lexical_ordering=lexical_ordering,
    )
