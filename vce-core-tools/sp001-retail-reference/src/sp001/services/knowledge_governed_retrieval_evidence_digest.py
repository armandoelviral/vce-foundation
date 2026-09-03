from dataclasses import dataclass

import hashlib

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
    canonical_knowledge_governed_retrieval_evidence_payload_bytes,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceDigest:
    """Immutable content identity without authenticity claims."""

    algorithm: str
    encoding: str
    value: str


def digest_knowledge_governed_retrieval_evidence(
    *,
    evidence: KnowledgeGovernedRetrievalEvidence,
) -> KnowledgeGovernedRetrievalEvidenceDigest:
    """Digest exact canonical retrieval-evidence payload bytes."""

    if not isinstance(
        evidence,
        KnowledgeGovernedRetrievalEvidence,
    ):
        raise TypeError(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        )

    payload_bytes = (
        canonical_knowledge_governed_retrieval_evidence_payload_bytes(
            evidence=evidence,
        )
    )
    value = hashlib.sha256(
        payload_bytes
    ).hexdigest()

    return KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm="SHA-256",
        encoding=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING
        ),
        value=value,
    )
