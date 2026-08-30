import hmac
import json

from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_serialization import (
    serialize_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_verification import (
    verify_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
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


def deserialize_knowledge_ingestion_registry_artifact(
    *,
    stored_artifact: str,
) -> KnowledgeIngestionRegistryArtifact:
    """Reconstruct and verify one canonical stored artifact envelope."""

    if not isinstance(
        stored_artifact,
        str,
    ):
        raise TypeError(
            "stored_artifact must be a string"
        )

    if not stored_artifact.strip():
        raise ValueError(
            "stored_artifact must not be empty"
        )

    try:
        document = json.loads(
            stored_artifact,
            object_pairs_hook=_unique_object,
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            "stored_artifact must contain valid JSON"
        ) from error

    if not isinstance(
        document,
        dict,
    ):
        raise ValueError(
            "stored_artifact must contain a JSON object"
        )

    _validate_exact_fields(
        document=document,
        expected=STORAGE_ENVELOPE_FIELDS,
        subject="storage envelope",
    )

    digest_document = document[
        "digest"
    ]

    if not isinstance(
        digest_document,
        dict,
    ):
        raise ValueError(
            "stored digest must be a JSON object"
        )

    _validate_exact_fields(
        document=digest_document,
        expected=STORAGE_DIGEST_FIELDS,
        subject="stored digest",
    )

    digest = KnowledgeIngestionRegistryDigest(
        algorithm=digest_document["algorithm"],
        encoding=digest_document["encoding"],
        value=digest_document["value"],
    )

    artifact = KnowledgeIngestionRegistryArtifact(
        payload=document["payload"],
        digest=digest,
        media_type=document["media_type"],
        schema_version=document["schema_version"],
    )

    verified = verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    if verified is not True:
        raise ValueError(
            "stored artifact integrity verification failed"
        )

    canonical = serialize_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    if not hmac.compare_digest(
        canonical.encode("UTF-8"),
        stored_artifact.encode("UTF-8"),
    ):
        raise ValueError(
            "stored artifact must use canonical JSON"
        )

    return artifact


def _unique_object(
    pairs: list[tuple[str, object]],
) -> dict:
    document = {}

    for key, value in pairs:
        if key in document:
            raise ValueError(
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
    present = frozenset(
        document
    )

    missing = expected - present

    if missing:
        raise ValueError(
            f"missing required {subject} fields: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    unexpected = present - expected

    if unexpected:
        raise ValueError(
            f"unexpected {subject} fields: "
            + ", ".join(
                sorted(
                    unexpected
                )
            )
        )
