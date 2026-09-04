import json

from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_verification import (
    verify_received_knowledge_governed_retrieval_evidence_artifact,
)


def serialize_knowledge_governed_retrieval_evidence_artifact(
    *,
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact,
) -> str:
    """Serialize one verified artifact as a canonical storage envelope."""
    if not isinstance(
        artifact,
        KnowledgeGovernedRetrievalEvidenceArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "KnowledgeGovernedRetrievalEvidenceArtifact"
        )
    verified = (
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )
    )
    if verified is not True:
        raise ValueError(
            "artifact verification failed"
        )
    document = {
        "digest": {
            "algorithm": artifact.digest.algorithm,
            "encoding": artifact.digest.encoding,
            "value": artifact.digest.value,
        },
        "media_type": artifact.media_type,
        "payload": artifact.payload,
        "schema_version": artifact.schema_version,
    }
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
