from dataclasses import FrozenInstanceError, fields
import json
from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_read import (
    KnowledgeGovernedRetrievalEvidenceReadResult,
    KnowledgeGovernedRetrievalEvidenceReadStatus,
    read_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_atomic_write import (
    write_knowledge_governed_retrieval_evidence_artifact,
)
from test_knowledge_governed_retrieval_evidence_artifact import (
    create_artifact,
)


def create_location(
    tmp_path: Path,
    *,
    logical_name: str = "retrieval-run-001",
) -> KnowledgeGovernedRetrievalEvidenceStorageLocation:
    return KnowledgeGovernedRetrievalEvidenceStorageLocation(
        storage_root=tmp_path / "retrieval-evidence-storage",
        logical_name=logical_name,
    )


def write_artifact(
    tmp_path: Path,
    *,
    artifact: KnowledgeGovernedRetrievalEvidenceArtifact | None = None,
) -> tuple[
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
    KnowledgeGovernedRetrievalEvidenceArtifact,
]:
    location = create_location(
        tmp_path,
    )
    selected = (
        artifact
        if artifact is not None
        else create_artifact()
    )
    write_knowledge_governed_retrieval_evidence_artifact(
        location=location,
        artifact=selected,
    )
    return location, selected


def test_read_status_vocabulary_is_exact() -> None:
    assert tuple(
        status.value
        for status in KnowledgeGovernedRetrievalEvidenceReadStatus
    ) == (
        "LOADED",
        "NOT_FOUND",
    )


def test_read_result_is_immutable(
    tmp_path: Path,
) -> None:
    result = KnowledgeGovernedRetrievalEvidenceReadResult(
        status=KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND,
        artifact_path=create_location(tmp_path).artifact_path,
        artifact=None,
    )
    with pytest.raises(
        FrozenInstanceError,
    ):
        result.status = KnowledgeGovernedRetrievalEvidenceReadStatus.LOADED


def test_read_result_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceReadResult
        )
    ) == (
        "status",
        "artifact_path",
        "artifact",
    )


def test_read_result_rejects_untyped_status(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceReadStatus",
    ):
        KnowledgeGovernedRetrievalEvidenceReadResult(
            status="NOT_FOUND",
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
        )


def test_read_result_rejects_untyped_artifact_path() -> None:
    with pytest.raises(
        TypeError,
        match="artifact_path must be a Path",
    ):
        KnowledgeGovernedRetrievalEvidenceReadResult(
            status=KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND,
            artifact_path="/retrieval-evidence/retrieval-run-001.retrieval-evidence.json",
            artifact=None,
        )


def test_read_result_rejects_relative_artifact_path() -> None:
    with pytest.raises(
        ValueError,
        match="artifact_path must be absolute",
    ):
        KnowledgeGovernedRetrievalEvidenceReadResult(
            status=KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND,
            artifact_path=Path("retrieval-run-001.retrieval-evidence.json"),
            artifact=None,
        )


def test_loaded_result_requires_artifact(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="LOADED requires",
    ):
        KnowledgeGovernedRetrievalEvidenceReadResult(
            status=KnowledgeGovernedRetrievalEvidenceReadStatus.LOADED,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
        )


def test_not_found_result_forbids_artifact(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="NOT_FOUND must not contain",
    ):
        KnowledgeGovernedRetrievalEvidenceReadResult(
            status=KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=create_artifact(),
        )


@pytest.mark.parametrize(
    "location",
    (
        None,
        "location",
        Path("/tmp/registry"),
        object(),
    ),
)
def test_reader_rejects_untyped_location(
    location: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceStorageLocation",
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_missing_artifact_returns_not_found(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    result = read_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceReadStatus.NOT_FOUND
    )
    assert result.artifact_path == location.artifact_path
    assert result.artifact is None


def test_missing_read_performs_no_filesystem_mutation(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    assert not location.storage_root.exists()
    read_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert not location.storage_root.exists()


def test_written_artifact_is_loaded(
    tmp_path: Path,
) -> None:
    location, artifact = write_artifact(
        tmp_path,
    )
    result = read_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceReadStatus.LOADED
    )
    assert result.artifact_path == location.artifact_path
    assert result.artifact == artifact


def test_loaded_artifact_preserves_unicode(
    tmp_path: Path,
) -> None:
    artifact = create_artifact(
        raw_text="planograma gobernado Ñ",
    )
    location, _ = write_artifact(
        tmp_path,
        artifact=artifact,
    )
    result = read_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.artifact == artifact
    assert "planograma gobernado Ñ" in result.artifact.payload


def test_reader_rejects_truncated_artifact(
    tmp_path: Path,
) -> None:
    location, _ = write_artifact(
        tmp_path,
    )
    stored = location.artifact_path.read_text(
        encoding="UTF-8",
    )
    location.artifact_path.write_text(
        stored[:-1],
        encoding="UTF-8",
    )
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_reader_rejects_non_utf8_bytes(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    location.storage_root.mkdir(
        parents=True,
    )
    location.artifact_path.write_bytes(
        b"\xff\xfe\xfd",
    )
    with pytest.raises(
        UnicodeDecodeError,
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_reader_rejects_digest_mismatch(
    tmp_path: Path,
) -> None:
    location, _ = write_artifact(
        tmp_path,
    )
    document = json.loads(
        location.artifact_path.read_text(
            encoding="UTF-8",
        )
    )
    document["digest"]["value"] = "0" * 64
    location.artifact_path.write_text(
        json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ),
        encoding="UTF-8",
    )
    with pytest.raises(
        ValueError,
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_reader_rejects_noncanonical_storage_json(
    tmp_path: Path,
) -> None:
    location, _ = write_artifact(
        tmp_path,
    )
    stored = location.artifact_path.read_text(
        encoding="UTF-8",
    )
    location.artifact_path.write_text(
        "\n" + stored,
        encoding="UTF-8",
    )
    with pytest.raises(
        ValueError,
        match="canonical JSON",
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_reader_does_not_convert_directory_to_not_found(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    location.artifact_path.mkdir(
        parents=True,
    )
    with pytest.raises(
        IsADirectoryError,
    ):
        read_knowledge_governed_retrieval_evidence_artifact(
            location=location,
        )


def test_read_result_grants_no_truth_or_authenticity_claim() -> None:
    names = {
        field.name
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceReadResult
        )
    }
    assert "authentic" not in names
    assert "authoritative" not in names
    assert "truth" not in names
    assert "verified" not in names
