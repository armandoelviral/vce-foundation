import json

from sp001.services.knowledge_governed_retrieval_evidence_artifact_verification import (
    verify_received_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
)


def serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
    *,
    envelope: KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
) -> str:
    """Serialize a verified artifact exchange envelope canonically."""
    if not isinstance(
        envelope,
        KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
    ):
        raise TypeError(
            "envelope must be a "
            "KnowledgeGovernedRetrievalEvidenceExchangeEnvelope"
        )

    verified = (
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=envelope.artifact,
        )
    )
    if verified is not True:
        raise ValueError(
            "exchange envelope artifact must pass verification"
        )

    document = {
        "artifact": {
            "digest": {
                "algorithm": envelope.artifact.digest.algorithm,
                "encoding": envelope.artifact.digest.encoding,
                "value": envelope.artifact.digest.value,
            },
            "media_type": envelope.artifact.media_type,
            "payload": envelope.artifact.payload,
            "schema_version": envelope.artifact.schema_version,
        },
        "encoding": envelope.encoding,
        "media_type": envelope.media_type,
        "protocol": envelope.protocol,
        "protocol_version": envelope.protocol_version,
    }

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes(
    *,
    envelope: KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
) -> bytes:
    """Encode the exact canonical exchange envelope as UTF-8 bytes."""
    serialized = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    return serialized.encode(
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    )
