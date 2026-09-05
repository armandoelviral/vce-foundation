import hmac

from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_parsing import (
    parse_received_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_serialization import (
    canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes,
)


class KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError(ValueError):
    """Base failure while accepting a received exchange envelope."""


class InvalidRetrievalEvidenceExchangeArtifactError(
    KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError
):
    """The parsed exchange contains an artifact that cannot be verified."""


class NoncanonicalRetrievalEvidenceExchangeEnvelopeError(
    KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError
):
    """The received exchange bytes differ from canonical exchange bytes."""


def accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
    *,
    received_envelope: str,
) -> KnowledgeGovernedRetrievalEvidenceExchangeEnvelope:
    """Accept exact canonical exchange bytes containing a verified artifact."""
    if not isinstance(received_envelope, str):
        raise TypeError("received_envelope must be a string")

    received_bytes = received_envelope.encode(
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    )
    envelope = (
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received_envelope,
        )
    )

    try:
        canonical_bytes = (
            canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes(
                envelope=envelope,
            )
        )
    except (TypeError, ValueError) as error:
        raise InvalidRetrievalEvidenceExchangeArtifactError(
            str(error)
        ) from error

    if not hmac.compare_digest(
        received_bytes,
        canonical_bytes,
    ):
        raise NoncanonicalRetrievalEvidenceExchangeEnvelopeError(
            "received exchange envelope must be canonical UTF-8 JSON"
        )

    return envelope
