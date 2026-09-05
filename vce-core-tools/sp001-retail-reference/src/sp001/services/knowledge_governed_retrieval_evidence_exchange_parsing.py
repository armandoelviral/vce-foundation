import json
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
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION,
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
)


class KnowledgeGovernedRetrievalEvidenceExchangeParsingError(ValueError):
    """Base failure while parsing an untrusted exchange envelope."""


class MalformedRetrievalEvidenceExchangeEnvelopeError(
    KnowledgeGovernedRetrievalEvidenceExchangeParsingError
):
    """The received exchange text is not unique-field JSON."""


class InvalidRetrievalEvidenceExchangeStructureError(
    KnowledgeGovernedRetrievalEvidenceExchangeParsingError
):
    """The received exchange document has an invalid closed shape."""


class UnsupportedRetrievalEvidenceExchangeMetadataError(
    KnowledgeGovernedRetrievalEvidenceExchangeParsingError
):
    """The received exchange document uses unsupported metadata."""


class _DuplicateExchangeFieldError(ValueError):
    pass


def parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
    *,
    received_envelope: str,
) -> KnowledgeGovernedRetrievalEvidenceExchangeEnvelope:
    """Parse an exchange envelope without accepting artifact integrity."""
    if not isinstance(received_envelope, str):
        raise TypeError("received_envelope must be a string")

    try:
        document = json.loads(
            received_envelope,
            object_pairs_hook=_unique_object,
        )
    except (json.JSONDecodeError, _DuplicateExchangeFieldError) as error:
        raise MalformedRetrievalEvidenceExchangeEnvelopeError(
            str(error)
        ) from error

    _require_object(
        value=document,
        keys={
            "artifact",
            "encoding",
            "media_type",
            "protocol",
            "protocol_version",
        },
        path="exchange envelope",
    )
    artifact_document = document["artifact"]
    _require_object(
        value=artifact_document,
        keys={
            "digest",
            "media_type",
            "payload",
            "schema_version",
        },
        path="artifact",
    )
    digest_document = artifact_document["digest"]
    _require_object(
        value=digest_document,
        keys={"algorithm", "encoding", "value"},
        path="artifact.digest",
    )

    _require_metadata(
        value=document["protocol"],
        expected=KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL,
        path="protocol",
    )
    _require_strict_integer_metadata(
        value=document["protocol_version"],
        expected=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION
        ),
        path="protocol_version",
    )
    _require_metadata(
        value=document["media_type"],
        expected=(
            KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE
        ),
        path="media_type",
    )
    _require_metadata(
        value=document["encoding"],
        expected=KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
        path="encoding",
    )
    _require_metadata(
        value=artifact_document["media_type"],
        expected=KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE,
        path="artifact.media_type",
    )
    _require_strict_integer_metadata(
        value=artifact_document["schema_version"],
        expected=KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
        path="artifact.schema_version",
    )
    _require_metadata(
        value=digest_document["algorithm"],
        expected="SHA-256",
        path="artifact.digest.algorithm",
    )
    _require_metadata(
        value=digest_document["encoding"],
        expected=KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
        path="artifact.digest.encoding",
    )

    payload = artifact_document["payload"]
    if not isinstance(payload, str):
        raise InvalidRetrievalEvidenceExchangeStructureError(
            "artifact.payload must be a string"
        )
    digest_value = digest_document["value"]
    if (
        not isinstance(digest_value, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest_value) is None
    ):
        raise InvalidRetrievalEvidenceExchangeStructureError(
            "artifact.digest.value must contain "
            "64 lowercase hexadecimal characters"
        )

    digest = KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm=digest_document["algorithm"],
        encoding=digest_document["encoding"],
        value=digest_value,
    )
    artifact = KnowledgeGovernedRetrievalEvidenceArtifact(
        payload=payload,
        digest=digest,
        media_type=artifact_document["media_type"],
        schema_version=artifact_document["schema_version"],
    )
    return KnowledgeGovernedRetrievalEvidenceExchangeEnvelope(
        protocol=document["protocol"],
        protocol_version=document["protocol_version"],
        media_type=document["media_type"],
        encoding=document["encoding"],
        artifact=artifact,
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    document = {}
    for key, value in pairs:
        if key in document:
            raise _DuplicateExchangeFieldError(
                f"duplicate exchange field: {key}"
            )
        document[key] = value
    return document


def _require_object(
    *,
    value: object,
    keys: set[str],
    path: str,
) -> None:
    if not isinstance(value, dict):
        raise InvalidRetrievalEvidenceExchangeStructureError(
            f"{path} must be an object"
        )
    actual = set(value)
    if actual != keys:
        raise InvalidRetrievalEvidenceExchangeStructureError(
            f"{path} fields must be exactly {sorted(keys)}"
        )


def _require_metadata(
    *,
    value: object,
    expected: str,
    path: str,
) -> None:
    if not isinstance(value, str):
        raise InvalidRetrievalEvidenceExchangeStructureError(
            f"{path} must be a string"
        )
    if value != expected:
        raise UnsupportedRetrievalEvidenceExchangeMetadataError(
            f"unsupported {path}: {value}"
        )


def _require_strict_integer_metadata(
    *,
    value: object,
    expected: int,
    path: str,
) -> None:
    if type(value) is not int:
        raise InvalidRetrievalEvidenceExchangeStructureError(
            f"{path} must be an integer"
        )
    if value != expected:
        raise UnsupportedRetrievalEvidenceExchangeMetadataError(
            f"unsupported {path}: {value}"
        )
