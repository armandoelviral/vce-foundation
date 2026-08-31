from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
)
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KnowledgeCandidateLexicalOrderingEvidence,
)


def materialize_knowledge_candidate_lexical_ordering_evidence(
    *,
    match: KnowledgeCandidateLexicalMatch,
) -> KnowledgeCandidateLexicalOrderingEvidence:
    """Materialize one canonical lexical ordering key."""

    if not isinstance(
        match,
        KnowledgeCandidateLexicalMatch,
    ):
        raise TypeError(
            "match must be a KnowledgeCandidateLexicalMatch"
        )

    return KnowledgeCandidateLexicalOrderingEvidence(
        match=match,
    )
