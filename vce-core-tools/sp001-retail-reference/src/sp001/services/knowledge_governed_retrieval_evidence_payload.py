from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)


KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING = "UTF-8"


def canonical_knowledge_governed_retrieval_evidence_payload_bytes(
    *,
    evidence: KnowledgeGovernedRetrievalEvidence,
) -> bytes:
    """Return exact canonical retrieval-evidence payload bytes."""

    if not isinstance(
        evidence,
        KnowledgeGovernedRetrievalEvidence,
    ):
        raise TypeError(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        )

    payload = serialize_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    return payload.encode(
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
    )
