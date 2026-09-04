from dataclasses import dataclass
import os
from pathlib import Path
import tempfile

from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization import (
    serialize_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)


@dataclass(frozen=True, slots=True)
class KnowledgeGovernedRetrievalEvidenceWriteResult:
    """Completed atomic write facts without authority claims."""

    artifact_path: Path
    digest: KnowledgeGovernedRetrievalEvidenceDigest
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
            KnowledgeGovernedRetrievalEvidenceDigest,
        ):
            raise TypeError(
                "digest must be a "
                "KnowledgeGovernedRetrievalEvidenceDigest"
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


def write_knowledge_governed_retrieval_evidence_artifact(
    *,
    location: KnowledgeGovernedRetrievalEvidenceStorageLocation,
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact,
) -> KnowledgeGovernedRetrievalEvidenceWriteResult:
    """Verify and atomically replace one local evidence artifact."""
    if not isinstance(
        location,
        KnowledgeGovernedRetrievalEvidenceStorageLocation,
    ):
        raise TypeError(
            "location must be a "
            "KnowledgeGovernedRetrievalEvidenceStorageLocation"
        )
    if not isinstance(
        artifact,
        KnowledgeGovernedRetrievalEvidenceArtifact,
    ):
        raise TypeError(
            "artifact must be a "
            "KnowledgeGovernedRetrievalEvidenceArtifact"
        )
    stored_artifact = (
        serialize_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )
    )
    content = stored_artifact.encode(
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
    return KnowledgeGovernedRetrievalEvidenceWriteResult(
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
