from dataclasses import dataclass

from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)


KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL = (
    "sp001.knowledge-governed-retrieval-evidence"
)
KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION = 1
KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE = (
    "application/vnd.sp001.knowledge-governed-retrieval-evidence+json"
)
KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING = "UTF-8"


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceExchangeEnvelope:
    """Self-describing exchange package without delivery or trust claims."""

    protocol: str
    protocol_version: int
    media_type: str
    encoding: str
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact

    def __post_init__(self) -> None:
        if not isinstance(
            self.protocol,
            str,
        ):
            raise TypeError(
                "protocol must be a string"
            )
        if self.protocol != (
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL
        ):
            raise ValueError(
                "protocol must equal supported governed retrieval "
                "evidence exchange protocol"
            )
        if type(self.protocol_version) is not int:
            raise TypeError(
                "protocol_version must be an integer"
            )
        if self.protocol_version != (
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION
        ):
            raise ValueError(
                "protocol_version must equal supported version 1"
            )
        if not isinstance(
            self.media_type,
            str,
        ):
            raise TypeError(
                "media_type must be a string"
            )
        if self.media_type != (
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE
        ):
            raise ValueError(
                "media_type must equal supported exchange media type"
            )
        if not isinstance(
            self.encoding,
            str,
        ):
            raise TypeError(
                "encoding must be a string"
            )
        if self.encoding != (
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING
        ):
            raise ValueError(
                "encoding must be UTF-8"
            )
        if not isinstance(
            self.artifact,
            KnowledgeGovernedRetrievalEvidenceArtifact,
        ):
            raise TypeError(
                "artifact must be a "
                "KnowledgeGovernedRetrievalEvidenceArtifact"
            )


def build_knowledge_governed_retrieval_evidence_exchange_envelope(
    *,
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact,
) -> KnowledgeGovernedRetrievalEvidenceExchangeEnvelope:
    """Package a typed artifact with fixed exchange protocol metadata."""
    return KnowledgeGovernedRetrievalEvidenceExchangeEnvelope(
        protocol=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL
        ),
        protocol_version=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION
        ),
        media_type=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE
        ),
        encoding=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING
        ),
        artifact=artifact,
    )
