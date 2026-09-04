from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_read import (
    KnowledgeGovernedRetrievalEvidenceReadStatus,
    read_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_deserialization import (
    InvalidRetrievalEvidenceStorageStructureError,
    MalformedRetrievalEvidenceStorageError,
    NoncanonicalRetrievalEvidenceStorageError,
    RetrievalEvidenceStorageIntegrityMismatchError,
)


class KnowledgeGovernedRetrievalEvidenceRecoveryStatus(StrEnum):
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
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_ENCODING,
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.MALFORMED_STORAGE,
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_STRUCTURE,
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INTEGRITY_MISMATCH,
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NONCANONICAL_STORAGE,
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE,
    )
)


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceRecoveryResult:
    """Auditable recovery classification without filesystem mutation."""

    status: KnowledgeGovernedRetrievalEvidenceRecoveryStatus
    artifact_path: Path
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact | None
    failure_type: str | None
    failure_detail: str | None

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus,
        ):
            raise TypeError(
                "status must be a "
                "KnowledgeGovernedRetrievalEvidenceRecoveryStatus"
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
            is KnowledgeGovernedRetrievalEvidenceRecoveryStatus.RECOVERED
        ):
            if not isinstance(
                self.artifact,
                KnowledgeGovernedRetrievalEvidenceArtifact,
            ):
                raise ValueError(
                    "RECOVERED requires a "
                    "KnowledgeGovernedRetrievalEvidenceArtifact"
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
            is KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND
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


def recover_knowledge_governed_retrieval_evidence_artifact(
    *,
    location: KnowledgeGovernedRetrievalEvidenceStorageLocation,
) -> KnowledgeGovernedRetrievalEvidenceRecoveryResult:
    """Classify one local read without repairing or replacing storage."""
    if not isinstance(
        location,
        KnowledgeGovernedRetrievalEvidenceStorageLocation,
    ):
        raise TypeError(
            "location must be a "
            "KnowledgeGovernedRetrievalEvidenceStorageLocation"
        )
    artifact_path = location.artifact_path
    try:
        read_result = (
            read_knowledge_governed_retrieval_evidence_artifact(
                location=location,
            )
        )
    except UnicodeDecodeError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_ENCODING
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except MalformedRetrievalEvidenceStorageError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.MALFORMED_STORAGE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except InvalidRetrievalEvidenceStorageStructureError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_STRUCTURE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except RetrievalEvidenceStorageIntegrityMismatchError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INTEGRITY_MISMATCH
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except NoncanonicalRetrievalEvidenceStorageError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NONCANONICAL_STORAGE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    except OSError as error:
        return _failure_result(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE
            ),
            artifact_path=artifact_path,
            error=error,
        )
    if (
        read_result.status
        is KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND
    ):
        return KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=(
                KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND
            ),
            artifact_path=artifact_path,
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )
    return KnowledgeGovernedRetrievalEvidenceRecoveryResult(
        status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.RECOVERED,
        artifact_path=artifact_path,
        artifact=read_result.artifact,
        failure_type=None,
        failure_detail=None,
    )


def _failure_result(
    *,
    status: KnowledgeGovernedRetrievalEvidenceRecoveryStatus,
    artifact_path: Path,
    error: Exception,
) -> KnowledgeGovernedRetrievalEvidenceRecoveryResult:
    failure_type = type(
        error
    ).__name__
    failure_detail = (
        str(error)
        or failure_type
    )
    return KnowledgeGovernedRetrievalEvidenceRecoveryResult(
        status=status,
        artifact_path=artifact_path,
        artifact=None,
        failure_type=failure_type,
        failure_detail=failure_detail,
    )
