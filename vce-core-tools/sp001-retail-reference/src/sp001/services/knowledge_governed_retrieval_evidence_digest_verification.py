import hmac
import re

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
    digest_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
)


def verify_knowledge_governed_retrieval_evidence_digest(
    *,
    evidence: KnowledgeGovernedRetrievalEvidence,
    digest: KnowledgeGovernedRetrievalEvidenceDigest,
) -> bool:
    """Verify content correspondence without asserting authenticity."""

    if not isinstance(
        evidence,
        KnowledgeGovernedRetrievalEvidence,
    ):
        raise TypeError(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        )

    if not isinstance(
        digest,
        KnowledgeGovernedRetrievalEvidenceDigest,
    ):
        raise TypeError(
            "digest must be a "
            "KnowledgeGovernedRetrievalEvidenceDigest"
        )

    if digest.algorithm != "SHA-256":
        raise ValueError(
            "digest algorithm must be SHA-256"
        )

    if (
        digest.encoding
        != KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING
    ):
        raise ValueError(
            "digest encoding must be UTF-8"
        )

    if (
        not isinstance(
            digest.value,
            str,
        )
        or re.fullmatch(
            r"[0-9a-f]{64}",
            digest.value,
        )
        is None
    ):
        raise ValueError(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        )

    expected = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    return hmac.compare_digest(
        expected.value,
        digest.value,
    )
