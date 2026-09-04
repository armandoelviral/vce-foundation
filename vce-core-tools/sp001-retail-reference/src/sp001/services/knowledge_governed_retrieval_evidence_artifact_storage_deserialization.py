import hmac
import json

from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization import (
    serialize_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_verification import (
    verify_received_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)


STORAGE_ENVELOPE_FIELDS = frozenset(
    (
        "digest",
        "media_type",
        "payload",
        "schema_version",
    )
)
STORAGE_DIGEST_FIELDS = frozenset(
    (
        "algorithm",
        "encoding",
        "value",
    )
)


class KnowledgeGovernedRetrievalEvidenceStorageError(ValueError):
    """Base error for invalid persisted retrieval evidence."""


class MalformedRetrievalEvidenceStorageError(
    KnowledgeGovernedRetrievalEvidenceStorageError
):
    """Stored text is empty or is not syntactically valid JSON."""


class InvalidRetrievalEvidenceStorageStructureError(
    KnowledgeGovernedRetrievalEvidenceStorageError
):
    """Stored JSON cannot represent a supported evidence artifact."""


class RetrievalEvidenceStorageIntegrityMismatchError(
    KnowledgeGovernedRetrievalEvidenceStorageError
):
    """Stored payload bytes do not correspond to the declared digest."""


class NoncanonicalRetrievalEvidenceStorageError(
    KnowledgeGovernedRetrievalEvidenceStorageError
):
    """Stored evidence is valid but not in canonical storage form."""


def deserialize_knowledge_governed_retrieval_evidence_artifact(
    *,
    stored_artifact: str,
) -> KnowledgeGovernedRetrievalEvidenceArtifact:
    """Reconstruct and verify one canonical stored evidence envelope."""
    if not isinstance(
        stored_artifact,
        str,
    ):
        raise TypeError(
            "stored_artifact must be a string"
        )
    if not stored_artifact.strip():
        raise MalformedRetrievalEvidenceStorageError(
            "stored_artifact must not be empty"
        )
    try:
        document = json.loads(
            stored_artifact,
            object_pairs_hook=_unique_object,
        )
    except json.JSONDecodeError as error:
        raise MalformedRetrievalEvidenceStorageError(
            "stored_artifact must contain valid JSON"
        ) from error
    if not isinstance(
        document,
        dict,
    ):
        raise InvalidRetrievalEvidenceStorageStructureError(
            "stored_artifact must contain a JSON object"
        )
    _validate_exact_fields(
        document=document,
        expected=STORAGE_ENVELOPE_FIELDS,
        subject="storage envelope",
    )
    digest_document = document["digest"]
    if not isinstance(
        digest_document,
        dict,
    ):
        raise InvalidRetrievalEvidenceStorageStructureError(
            "stored digest must be a JSON object"
        )
    _validate_exact_fields(
        document=digest_document,
        expected=STORAGE_DIGEST_FIELDS,
        subject="stored digest",
    )
    try:
        digest = KnowledgeGovernedRetrievalEvidenceDigest(
            algorithm=digest_document["algorithm"],
            encoding=digest_document["encoding"],
            value=digest_document["value"],
        )
        artifact = KnowledgeGovernedRetrievalEvidenceArtifact(
            payload=document["payload"],
            digest=digest,
            media_type=document["media_type"],
            schema_version=document["schema_version"],
        )
        verified = (
            verify_received_knowledge_governed_retrieval_evidence_artifact(
                artifact=artifact,
            )
        )
    except (
        TypeError,
        ValueError,
    ) as error:
        raise InvalidRetrievalEvidenceStorageStructureError(
            str(error)
        ) from error
    if verified is not True:
        raise RetrievalEvidenceStorageIntegrityMismatchError(
            "stored artifact integrity verification failed"
        )
    canonical = (
        serialize_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )
    )
    if not hmac.compare_digest(
        canonical.encode("UTF-8"),
        stored_artifact.encode("UTF-8"),
    ):
        raise NoncanonicalRetrievalEvidenceStorageError(
            "stored artifact must use canonical JSON"
        )
    return artifact


def _unique_object(
    pairs: list[tuple[str, object]],
) -> dict:
    document = {}
    for key, value in pairs:
        if key in document:
            raise InvalidRetrievalEvidenceStorageStructureError(
                f"duplicate JSON field: {key}"
            )
        document[key] = value
    return document


def _validate_exact_fields(
    *,
    document: dict,
    expected: frozenset,
    subject: str,
) -> None:
    present = frozenset(document)
    missing = expected - present
    if missing:
        raise InvalidRetrievalEvidenceStorageStructureError(
            f"missing required {subject} fields: "
            + ", ".join(sorted(missing))
        )
    unexpected = present - expected
    if unexpected:
        raise InvalidRetrievalEvidenceStorageStructureError(
            f"unexpected {subject} fields: "
            + ", ".join(sorted(unexpected))
        )
