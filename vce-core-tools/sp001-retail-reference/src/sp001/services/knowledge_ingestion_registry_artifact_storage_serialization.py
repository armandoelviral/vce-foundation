import json

from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_verification import (
    verify_knowledge_ingestion_registry_artifact,
)


def serialize_knowledge_ingestion_registry_artifact(
    *,
    artifact: KnowledgeIngestionRegistryArtifact,
) -> str:
    """Serialize one verified artifact as a canonical storage envelope."""

    if not isinstance(
        artifact,
        KnowledgeIngestionRegistryArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "KnowledgeIngestionRegistryArtifact"
        )

    verified = verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    if verified is not True:
        raise ValueError(
            "artifact integrity verification failed"
        )

    document = {
        "digest": {
            "algorithm": artifact.digest.algorithm,
            "encoding": artifact.digest.encoding,
            "value": artifact.digest.value,
        },
        "media_type": artifact.media_type,
        "payload": artifact.payload,
        "schema_version": artifact.schema_version,
    }

    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
