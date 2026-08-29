import hmac
import re

from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRegistry,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
    digest_knowledge_ingestion_registry,
)


def verify_knowledge_ingestion_registry_digest(
    *,
    registry: KnowledgeIngestionRegistry,
    digest: KnowledgeIngestionRegistryDigest,
) -> bool:
    """Verify content correspondence without asserting authenticity."""

    if not isinstance(
        registry,
        KnowledgeIngestionRegistry,
    ):
        raise TypeError(
            "registry must be a KnowledgeIngestionRegistry"
        )

    if not isinstance(
        digest,
        KnowledgeIngestionRegistryDigest,
    ):
        raise TypeError(
            "digest must be a "
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

    expected = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    return hmac.compare_digest(
        expected.value,
        digest.value,
    )
