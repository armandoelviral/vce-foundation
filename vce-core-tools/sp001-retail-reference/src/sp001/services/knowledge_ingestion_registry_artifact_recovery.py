from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from sp001.contracts.knowledge_ingestion_registry_storage_location import (
    KnowledgeIngestionRegistryStorageLocation,
)
from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_read import (
    KnowledgeIngestionRegistryReadStatus,
    read_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_deserialization import (
    InvalidRegistryStorageStructureError,
    MalformedRegistryStorageError,
    NoncanonicalRegistryStorageError,
    RegistryStorageIntegrityMismatchError,
)


class KnowledgeIngestionRegistryRecoveryStatus(StrEnum):
    """Explicit local recovery outcome without repair claims."""

    RECOVERED = "RECOVERED"
    NOT_FOUND = "NOT_FOUND"
    INVALID_ENCODING = "INVALID_ENCODING"
    MALFORMED_STORAGE = "MALFORMED_STORAGE"
    INVALID_STRUCTURE = "INVALID_STRUCTURE"
    INTEGRITY_MISMATCH = "INTEGRITY_MISMATCH"
    NONCANONICAL_STORAGE = "NONCANONICAL_STORAGE"
    IO_FAILURE = "IO_FAILURE"


FAILURE_STATUSES = frozenset(
    (
        KnowledgeIngestionRegistryRecoveryStatus.INVALID_ENCODING,
        KnowledgeIngestionRegistryRecoveryStatus.MALFORMED_STORAGE,
        KnowledgeIngestionRegistryRecoveryStatus.INVALID_STRUCTURE,
        KnowledgeIngestionRegistryRecoveryStatus.INTEGRITY_MISMATCH,
        KnowledgeIngestionRegistryRecoveryStatus.NONCANONICAL_STORAGE,
        KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
    )
)


@dataclass(frozen=True, slots=True)
class KnowledgeIngestionRegistryRecoveryResult:
    """Auditable recovery classification without filesystem mutation."""

    status: KnowledgeIngestionRegistryRecoveryStatus
    artifact_path: Path
    artifact: KnowledgeIngestionRegistryArtifact | None
    failure_type: str | None
    failure_detail: str | None

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            KnowledgeIngestionRegistryRecoveryStatus,
        ):
            raise TypeError(
                "status must be a "
                "KnowledgeIngestionRegistryRecoveryStatus"
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
            is KnowledgeIngestionRegistryRecoveryStatus.RECOVERED
        ):
            if not isinstance(
                self.artifact,
                KnowledgeIngestionRegistryArtifact,
            ):
                raise ValueError(
                    "RECOVERED requires a "
                    "KnowledgeIngestionRegistryArtifact"
                )
            if (
                self.failure_type is not None
                or self.failure_detail is not None
            ):
                raise ValueError(
                    "RECOVERED must not contain failure details"
                )
            return

        if self.artifact is not None:
            raise ValueError(
                "non-recovered status must not contain an artifact"
            )

        if (
            self.status
            is KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND
        ):
            if (
                self.failure_type is not None
                or self.failure_detail is not None
            ):
                raise ValueError(
                    "NOT_FOUND must not contain failure details"
                )
            return

        if self.status not in FAILURE_STATUSES:
            raise ValueError(
                "unsupported recovery status"
            )
        if (
            not isinstance(
                self.failure_type,
                str,
            )
            or not self.failure_type
        ):
            raise ValueError(
                "failure status requires failure_type"
            )
        if (
            not isinstance(
                self.failure_detail,
                str,
            )
            or not self.failure_detail
        ):
            raise ValueError(
                "failure status requires failure_detail"
            )


def recover_knowledge_ingestion_registry_artifact(
    *,
    location: KnowledgeIngestionRegistryStorageLocation,
) -> KnowledgeIngestionRegistryRecoveryResult:
    """Classify one local read without repairing or replacing storage."""

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
        read_result = read_knowledge_ingestion_registry_artifact(
            location=location,
        )
    except UnicodeDecodeError as error:
        return _failure_result(
            status=(
                KnowledgeIngestionRegistryRecoveryStatus.INVALID_ENCODING
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except MalformedRegistryStorageError as error:
        return _failure_result(
            status=(
                KnowledgeIngestionRegistryRecoveryStatus.MALFORMED_STORAGE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except InvalidRegistryStorageStructureError as error:
        return _failure_result(
            status=(
                KnowledgeIngestionRegistryRecoveryStatus.INVALID_STRUCTURE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except RegistryStorageIntegrityMismatchError as error:
        return _failure_result(
            status=(
                KnowledgeIngestionRegistryRecoveryStatus.INTEGRITY_MISMATCH
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except NoncanonicalRegistryStorageError as error:
        return _failure_result(
            status=(
                KnowledgeIngestionRegistryRecoveryStatus.NONCANONICAL_STORAGE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except OSError as error:
        return _failure_result(
            status=KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
            artifact_path=artifact_path,
            error=error,
        )

    if (
        read_result.status
        is KnowledgeIngestionRegistryReadStatus.NOT_FOUND
    ):
        return KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND,
            artifact_path=artifact_path,
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )

    return KnowledgeIngestionRegistryRecoveryResult(
        status=KnowledgeIngestionRegistryRecoveryStatus.RECOVERED,
        artifact_path=artifact_path,
        artifact=read_result.artifact,
        failure_type=None,
        failure_detail=None,
    )


def _failure_result(
    *,
    status: KnowledgeIngestionRegistryRecoveryStatus,
    artifact_path: Path,
    error: Exception,
) -> KnowledgeIngestionRegistryRecoveryResult:
    failure_type = type(
        error
    ).__name__
    failure_detail = (
        str(error)
        or failure_type
    )

    return KnowledgeIngestionRegistryRecoveryResult(
        status=status,
        artifact_path=artifact_path,
        artifact=None,
        failure_type=failure_type,
        failure_detail=failure_detail,
    )
