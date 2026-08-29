from dataclasses import dataclass
import hashlib

from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRegistry,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    serialize_knowledge_ingestion_registry,
)


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryDigest:
    """Immutable registry content identity without authenticity claims."""

    algorithm: str
    encoding: str
    value: str


def digest_knowledge_ingestion_registry(
    *,
    registry: KnowledgeIngestionRegistry,
) -> KnowledgeIngestionRegistryDigest:
    """Digest canonical registry JSON encoded as UTF-8 bytes."""

    if not isinstance(
        registry,
        KnowledgeIngestionRegistry,
    ):
        raise TypeError(
            "registry must be a KnowledgeIngestionRegistry"
        )

    payload = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    value = hashlib.sha256(
        payload.encode(
            "utf-8",
        )
    ).hexdigest()

    return KnowledgeIngestionRegistryDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=value,
    )
