from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from sp001.contracts.knowledge_ingestion_registry_storage_location import (
    KnowledgeIngestionRegistryStorageLocation,
)
from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_deserialization import (
    deserialize_knowledge_ingestion_registry_artifact,
)


class KnowledgeIngestionRegistryReadStatus(StrEnum):
    """Filesystem read outcome without integrity or authority overclaim."""

    LOADED = "LOADED"
    NOT_FOUND = "NOT_FOUND"


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryReadResult:
    """Observed local read result for one deterministic artifact path."""

    status: KnowledgeIngestionRegistryReadStatus
    artifact_path: Path
    artifact: KnowledgeIngestionRegistryArtifact | None

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            KnowledgeIngestionRegistryReadStatus,
        ):
            raise TypeError(
                "status must be a "
                "KnowledgeIngestionRegistryReadStatus"
            )
        if not isinstance(
            self.artifact_path,
            Path,
        ):
            raise TypeError(
                "artifact_path must be a Path"
            )
        if not self.artifact_path.is_absolute():
            raise ValueError(
                "artifact_path must be absolute"
            )
        if (
            self.status
            is KnowledgeIngestionRegistryReadStatus.LOADED
        ):
            if not isinstance(
                self.artifact,
                KnowledgeIngestionRegistryArtifact,
            ):
                raise ValueError(
                    "LOADED requires a "
                    "KnowledgeIngestionRegistryArtifact"
                )
        elif self.artifact is not None:
            raise ValueError(
                "NOT_FOUND must not contain an artifact"
            )


def read_knowledge_ingestion_registry_artifact(
    *,
    location: KnowledgeIngestionRegistryStorageLocation,
) -> KnowledgeIngestionRegistryReadResult:
    """Read one local artifact and return it only after verification."""

    if not isinstance(
        location,
        KnowledgeIngestionRegistryStorageLocation,
    ):
        raise TypeError(
            "location must be a "
            "KnowledgeIngestionRegistryStorageLocation"
        )

    artifact_path = location.artifact_path

    try:
        stored_artifact = artifact_path.read_text(
            encoding="UTF-8",
        )
    except FileNotFoundError:
        return KnowledgeIngestionRegistryReadResult(
            status=(
                KnowledgeIngestionRegistryReadStatus.NOT_FOUND
            ),
            artifact_path=artifact_path,
            artifact=None,
        )

    artifact = (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored_artifact,
        )
    )

    return KnowledgeIngestionRegistryReadResult(
        status=KnowledgeIngestionRegistryReadStatus.LOADED,
        artifact_path=artifact_path,
        artifact=artifact,
    )
