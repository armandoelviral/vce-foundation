from dataclasses import dataclass

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
    digest_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)


KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE = (
    "application/json"
)


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceArtifact:
    """Immutable canonical payload package without authenticity claims."""

    payload: str
    digest: KnowledgeGovernedRetrievalEvidenceDigest
    media_type: str
    schema_version: int


def build_knowledge_governed_retrieval_evidence_artifact(
    *,
    evidence: KnowledgeGovernedRetrievalEvidence,
) -> KnowledgeGovernedRetrievalEvidenceArtifact:
    """Package validated evidence with its canonical content identity."""

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
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    return KnowledgeGovernedRetrievalEvidenceArtifact(
        payload=payload,
        digest=digest,
        media_type=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE
        ),
        schema_version=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
        ),
    )
