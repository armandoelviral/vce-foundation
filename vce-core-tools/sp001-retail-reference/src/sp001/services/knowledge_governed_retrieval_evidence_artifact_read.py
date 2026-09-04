from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_deserialization import (
    deserialize_knowledge_governed_retrieval_evidence_artifact,
)


class KnowledgeGovernedRetrievalEvidenceReadStatus(StrEnum):
    """Filesystem read outcome without integrity or authority overclaim."""

    LOADED = "LOADED"
    NOT_FOUND = "NOT_FOUND"


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceReadResult:
    """Observed local read result for one deterministic artifact path."""

    status: KnowledgeGovernedRetrievalEvidenceReadStatus
    artifact_path: Path
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact | None

    def __post_init__(self) -> None:
        if not isinstance(
            self.status,
            KnowledgeGovernedRetrievalEvidenceReadStatus,
        ):
            raise TypeError(
                "status must be a "
                "KnowledgeGovernedRetrievalEvidenceReadStatus"
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
            is KnowledgeGovernedRetrievalEvidenceReadStatus.LOADED
        ):
            if not isinstance(
                self.artifact,
                KnowledgeGovernedRetrievalEvidenceArtifact,
            ):
                raise ValueError(
                    "LOADED requires a "
                    "KnowledgeGovernedRetrievalEvidenceArtifact"
                )
        elif self.artifact is not None:
            raise ValueError(
                "NOT_FOUND must not contain an artifact"
            )


def read_knowledge_governed_retrieval_evidence_artifact(
    *,
    location: KnowledgeGovernedRetrievalEvidenceStorageLocation,
) -> KnowledgeGovernedRetrievalEvidenceReadResult:
    """Read one local artifact and return it only after verification."""
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
        stored_artifact = artifact_path.read_text(
            encoding="UTF-8",
        )
    except FileNotFoundError:
        return KnowledgeGovernedRetrievalEvidenceReadResult(
            status=(
                KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND
            ),
            artifact_path=artifact_path,
            artifact=None,
        )
    artifact = (
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=stored_artifact,
        )
    )
    return KnowledgeGovernedRetrievalEvidenceReadResult(
        status=KnowledgeGovernedRetrievalEvidenceReadStatus.LOADED,
        artifact_path=artifact_path,
        artifact=artifact,
    )
