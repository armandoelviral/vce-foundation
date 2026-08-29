from dataclasses import dataclass

from sp001.contracts.knowledge_ingestion_registry import (
    KnowledgeIngestionRegistry,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
    digest_knowledge_ingestion_registry,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION,
    serialize_knowledge_ingestion_registry,
)


KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE = "application/json"


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryArtifact:
    """Immutable registry exchange payload without authenticity claims."""

    payload: str
    digest: KnowledgeIngestionRegistryDigest
    media_type: str
    schema_version: int


def build_knowledge_ingestion_registry_artifact(
    *,
    registry: KnowledgeIngestionRegistry,
) -> KnowledgeIngestionRegistryArtifact:
    """Package canonical registry content and its byte identity."""

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

    digest = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    return KnowledgeIngestionRegistryArtifact(
        payload=payload,
        digest=digest,
        media_type=(
            KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE
        ),
        schema_version=(
            KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION
        ),
    )
