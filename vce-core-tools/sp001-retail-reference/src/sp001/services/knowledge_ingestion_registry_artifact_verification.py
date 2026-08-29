import hashlib
import hmac
import re

from sp001.services.knowledge_ingestion_registry_artifact import (
    KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE,
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
)
from sp001.services.knowledge_ingestion_registry_payload_validation import (
    validate_knowledge_ingestion_registry_payload,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION,
)


def verify_knowledge_ingestion_registry_artifact(
    *,
    artifact: KnowledgeIngestionRegistryArtifact,
) -> bool:
    """Verify exact received payload bytes, then validate structure."""

    if not isinstance(
        artifact,
        KnowledgeIngestionRegistryArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "KnowledgeIngestionRegistryArtifact"
        )

    if (
        artifact.media_type
        != KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE
    ):
        raise ValueError(
            "artifact media_type must be application/json"
        )

    if (
        isinstance(
            artifact.schema_version,
            bool,
        )
        or not isinstance(
            artifact.schema_version,
            int,
        )
        or artifact.schema_version
        != KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION
    ):
        raise ValueError(
            "artifact schema_version must equal supported version 1"
        )

    if not isinstance(
        artifact.payload,
        str,
    ):
        raise TypeError(
            "artifact payload must be a string"
        )

    if not artifact.payload.strip():
        raise ValueError(
            "artifact payload must not be empty"
        )

    digest = artifact.digest

    if not isinstance(
        digest,
        KnowledgeIngestionRegistryDigest,
    ):
        raise TypeError(
            "artifact digest must be a "
            "KnowledgeIngestionRegistryDigest"
        )

    if digest.algorithm != "SHA-256":
        raise ValueError(
            "digest algorithm must be SHA-256"
        )

    if digest.encoding != "UTF-8":
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

    expected = hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()

    integrity_verified = hmac.compare_digest(
        expected,
        digest.value,
    )

    if not integrity_verified:
        return False

    validate_knowledge_ingestion_registry_payload(
        payload=artifact.payload,
    )

    return True
