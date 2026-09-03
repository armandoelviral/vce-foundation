import hashlib
import hmac
import re

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE,
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload_validation import (
    validate_knowledge_governed_retrieval_evidence_payload,
)


def verify_received_knowledge_governed_retrieval_evidence_artifact(
    *,
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact,
) -> bool:
    """Verify exact received bytes before validating payload structure."""
    if not isinstance(
        artifact,
        KnowledgeGovernedRetrievalEvidenceArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "KnowledgeGovernedRetrievalEvidenceArtifact"
        )
    if artifact.media_type != (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE
    ):
        raise ValueError(
            "artifact media_type must be application/json"
        )
    if (
        type(artifact.schema_version) is not int
        or artifact.schema_version
        != KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
    ):
        raise ValueError(
            "artifact schema_version must equal supported version 1"
        )
    if not isinstance(
        artifact.digest,
        KnowledgeGovernedRetrievalEvidenceDigest,
    ):
        raise TypeError(
            "artifact digest must be a "
            "KnowledgeGovernedRetrievalEvidenceDigest"
        )
    if artifact.digest.algorithm != "SHA-256":
        raise ValueError(
            "digest algorithm must be SHA-256"
        )
    if artifact.digest.encoding != (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING
    ):
        raise ValueError(
            "digest encoding must be UTF-8"
        )
    if (
        not isinstance(
            artifact.digest.value,
            str,
        )
        or re.fullmatch(
            r"[0-9a-f]{64}",
            artifact.digest.value,
        )
        is None
    ):
        raise ValueError(
            "digest value must contain "
            "64 lowercase hexadecimal characters"
        )
    if not isinstance(
        artifact.payload,
        str,
    ):
        raise TypeError(
            "artifact payload must be a string"
        )
    try:
        received_bytes = artifact.payload.encode(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
            errors="strict",
        )
    except UnicodeEncodeError as error:
        raise ValueError(
            "artifact payload must be valid UTF-8"
        ) from error
    received_digest = hashlib.sha256(
        received_bytes
    ).hexdigest()
    if not hmac.compare_digest(
        received_digest,
        artifact.digest.value,
    ):
        return False
    return validate_knowledge_governed_retrieval_evidence_payload(
        payload=artifact.payload,
    )
