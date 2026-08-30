from dataclasses import dataclass
import os
from pathlib import Path
import tempfile

from sp001.contracts.knowledge_ingestion_registry_storage_location import (
    KnowledgeIngestionRegistryStorageLocation,
)
from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_verification import (
    verify_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
)


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryWriteResult:
    """Completed atomic write facts without authority claims."""

    artifact_path: Path
    digest: KnowledgeIngestionRegistryDigest
    bytes_written: int

    def __post_init__(self) -> None:
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

        if not isinstance(
            self.digest,
            KnowledgeIngestionRegistryDigest,
        ):
            raise TypeError(
                "digest must be a "
                "KnowledgeIngestionRegistryDigest"
            )

        if (
            isinstance(
                self.bytes_written,
                bool,
            )
            or not isinstance(
                self.bytes_written,
                int,
            )
            or self.bytes_written < 1
        ):
            raise ValueError(
                "bytes_written must be a positive integer"
            )


def write_knowledge_ingestion_registry_artifact(
    *,
    location: KnowledgeIngestionRegistryStorageLocation,
    artifact: KnowledgeIngestionRegistryArtifact,
) -> KnowledgeIngestionRegistryWriteResult:
    """Verify and atomically replace one local registry artifact."""

    if not isinstance(
        location,
        KnowledgeIngestionRegistryStorageLocation,
    ):
        raise TypeError(
            "location must be a "
            "KnowledgeIngestionRegistryStorageLocation"
        )

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

    content = artifact.payload.encode(
        "utf-8",
    )

    storage_root = location.storage_root
    artifact_path = location.artifact_path

    storage_root.mkdir(
        mode=0o700,
        parents=True,
        exist_ok=True,
    )

    if artifact_path.parent != storage_root:
        raise ValueError(
            "artifact path must remain inside storage_root"
        )

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{location.logical_name}.",
            suffix=".tmp",
            dir=storage_root,
            delete=False,
        ) as temporary:
            temporary_path = Path(
                temporary.name,
            )

            temporary.write(
                content,
            )

            temporary.flush()

            os.fsync(
                temporary.fileno(),
            )

        os.replace(
            temporary_path,
            artifact_path,
        )

        temporary_path = None

        _synchronize_directory(
            storage_root,
        )

    finally:
        if (
            temporary_path is not None
            and temporary_path.exists()
        ):
            temporary_path.unlink()

    return KnowledgeIngestionRegistryWriteResult(
        artifact_path=artifact_path,
        digest=artifact.digest,
        bytes_written=len(
            content,
        ),
    )


def _synchronize_directory(
    directory: Path,
) -> None:
    flags = os.O_RDONLY

    if hasattr(
        os,
        "O_DIRECTORY",
    ):
        flags |= os.O_DIRECTORY

    descriptor = os.open(
        directory,
        flags,
    )

    try:
        os.fsync(
            descriptor,
        )
    finally:
        os.close(
            descriptor,
        )
