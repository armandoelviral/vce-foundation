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
from sp001.services.knowledge_governed_retrieval_evidence_artifact_recovery import (
    FAILURE_STATUSES,
    KnowledgeGovernedRetrievalEvidenceRecoveryResult,
    KnowledgeGovernedRetrievalEvidenceRecoveryStatus,
    recover_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_atomic_write import (
    write_knowledge_governed_retrieval_evidence_artifact,
)
from test_knowledge_governed_retrieval_evidence_artifact import (
    create_artifact,
)


def create_location(
    tmp_path: Path,
) -> KnowledgeGovernedRetrievalEvidenceStorageLocation:
    return KnowledgeGovernedRetrievalEvidenceStorageLocation(
        storage_root=tmp_path / "retrieval-evidence-storage",
        logical_name="retrieval-run-001",
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


def failure_result(
    tmp_path: Path,
    *,
    status: KnowledgeGovernedRetrievalEvidenceRecoveryStatus,
    failure_type: str = "Failure",
    failure_detail: str = "failure detail",
) -> KnowledgeGovernedRetrievalEvidenceRecoveryResult:
    return KnowledgeGovernedRetrievalEvidenceRecoveryResult(
        status=status,
        artifact_path=create_location(tmp_path).artifact_path,
        artifact=None,
        failure_type=failure_type,
        failure_detail=failure_detail,
    )


def test_recovery_status_vocabulary_is_exact() -> None:
    assert tuple(
        status.value
        for status in KnowledgeGovernedRetrievalEvidenceRecoveryStatus
    ) == (
        "RECOVERED",
        "NOT_FOUND",
        "INVALID_ENCODING",
        "MALFORMED_STORAGE",
        "INVALID_STRUCTURE",
        "INTEGRITY_MISMATCH",
        "NONCANONICAL_STORAGE",
        "IO_FAILURE",
    )


def test_failure_status_set_is_exact() -> None:
    assert FAILURE_STATUSES == frozenset(
        (
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_ENCODING,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.MALFORMED_STORAGE,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_STRUCTURE,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INTEGRITY_MISMATCH,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NONCANONICAL_STORAGE,
            KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE,
        )
    )


def test_recovery_result_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceRecoveryResult
        )
    ) == (
        "status",
        "artifact_path",
        "artifact",
        "failure_type",
        "failure_detail",
    )


def test_recovery_result_is_immutable(
    tmp_path: Path,
) -> None:
    result = failure_result(
        tmp_path,
        status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE,
    )
    with pytest.raises(
        FrozenInstanceError,
    ):
        result.failure_type = "Changed"


def test_recovery_result_rejects_untyped_status(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceRecoveryStatus",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status="NOT_FOUND",
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )


def test_recovery_result_rejects_untyped_path() -> None:
    with pytest.raises(
        TypeError,
        match="artifact_path must be a Path",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND,
            artifact_path="/retrieval-evidence/retrieval-run-001.retrieval-evidence.json",
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )


def test_recovery_result_rejects_relative_path() -> None:
    with pytest.raises(
        ValueError,
        match="artifact_path must be absolute",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND,
            artifact_path=Path("retrieval-run-001.retrieval-evidence.json"),
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )


def test_recovered_requires_artifact(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="RECOVERED requires",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.RECOVERED,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )


def test_recovered_forbids_failure_details(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="RECOVERED must not contain",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.RECOVERED,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=create_artifact(),
            failure_type="Failure",
            failure_detail="detail",
        )


def test_not_found_forbids_artifact(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="non-recovered status",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=create_artifact(),
            failure_type=None,
            failure_detail=None,
        )


def test_not_found_forbids_failure_details(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="NOT_FOUND must not contain",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
            failure_type="FileNotFoundError",
            failure_detail="missing",
        )


@pytest.mark.parametrize(
    "status",
    tuple(
        FAILURE_STATUSES
    ),
)
def test_failure_status_forbids_artifact(
    tmp_path: Path,
    status: KnowledgeGovernedRetrievalEvidenceRecoveryStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="non-recovered status",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=status,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=create_artifact(),
            failure_type="Failure",
            failure_detail="detail",
        )


@pytest.mark.parametrize(
    "failure_type",
    (
        None,
        "",
        1,
    ),
)
def test_failure_status_requires_failure_type(
    tmp_path: Path,
    failure_type: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="requires failure_type",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
            failure_type=failure_type,
            failure_detail="detail",
        )


@pytest.mark.parametrize(
    "failure_detail",
    (
        None,
        "",
        1,
    ),
)
def test_failure_status_requires_failure_detail(
    tmp_path: Path,
    failure_detail: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="requires failure_detail",
    ):
        KnowledgeGovernedRetrievalEvidenceRecoveryResult(
            status=KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE,
            artifact_path=create_location(tmp_path).artifact_path,
            artifact=None,
            failure_type="Failure",
            failure_detail=failure_detail,
        )


def test_written_artifact_is_recovered(
    tmp_path: Path,
) -> None:
    location, artifact = write_artifact(
        tmp_path,
    )
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.RECOVERED
    )
    assert result.artifact == artifact
    assert result.failure_type is None
    assert result.failure_detail is None


def test_missing_artifact_is_not_found(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NOT_FOUND
    )
    assert result.artifact is None
    assert result.failure_type is None
    assert result.failure_detail is None


def test_invalid_encoding_is_classified(
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
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_ENCODING
    )
    assert result.failure_type == "UnicodeDecodeError"
    assert result.artifact is None


def test_malformed_storage_is_classified(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    location.storage_root.mkdir(
        parents=True,
    )
    location.artifact_path.write_text(
        "{",
        encoding="UTF-8",
    )
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.MALFORMED_STORAGE
    )
    assert result.failure_type == "MalformedRetrievalEvidenceStorageError"
    assert result.artifact is None


def test_invalid_structure_is_classified(
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
    del document["digest"]
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
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INVALID_STRUCTURE
    )
    assert result.failure_type == (
        "InvalidRetrievalEvidenceStorageStructureError"
    )
    assert result.artifact is None


def test_integrity_mismatch_is_classified(
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
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.INTEGRITY_MISMATCH
    )
    assert result.failure_type == (
        "RetrievalEvidenceStorageIntegrityMismatchError"
    )
    assert result.artifact is None


def test_noncanonical_storage_is_classified(
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
    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.NONCANONICAL_STORAGE
    )
    assert result.failure_type == "NoncanonicalRetrievalEvidenceStorageError"
    assert result.artifact is None


def test_io_failure_is_classified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    location = create_location(
        tmp_path,
    )

    def fail_read(
        self: Path,
        *args: object,
        **kwargs: object,
    ) -> str:
        raise PermissionError(
            "read denied"
        )

    monkeypatch.setattr(
        Path,
        "read_text",
        fail_read,
    )

    result = recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeGovernedRetrievalEvidenceRecoveryStatus.IO_FAILURE
    )
    assert result.failure_type == "PermissionError"
    assert result.failure_detail == "read denied"
    assert result.artifact is None


def test_recovery_performs_no_mutation_for_missing_artifact(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )
    recover_knowledge_governed_retrieval_evidence_artifact(
        location=location,
    )
    assert not location.storage_root.exists()


def test_recovery_result_grants_no_repair_or_authority_claim() -> None:
    names = {
        field.name
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceRecoveryResult
        )
    }
    assert "repaired" not in names
    assert "authentic" not in names
    assert "authoritative" not in names
    assert "truth" not in names
