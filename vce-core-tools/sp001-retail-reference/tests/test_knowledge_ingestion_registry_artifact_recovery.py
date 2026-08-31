from dataclasses import FrozenInstanceError, fields
import json
from pathlib import Path

import pytest

from sp001.contracts.knowledge_ingestion_registry_storage_location import (
    KnowledgeIngestionRegistryStorageLocation,
)
from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_recovery import (
    FAILURE_STATUSES,
    KnowledgeIngestionRegistryRecoveryResult,
    KnowledgeIngestionRegistryRecoveryStatus,
    recover_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_atomic_write import (
    write_knowledge_ingestion_registry_artifact,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def create_location(
    tmp_path: Path,
) -> KnowledgeIngestionRegistryStorageLocation:
    return KnowledgeIngestionRegistryStorageLocation(
        storage_root=tmp_path / "registry-storage",
        logical_name="primary",
    )


def create_artifact(
    *,
    ingestion_id: str = "INGESTION-001",
) -> KnowledgeIngestionRegistryArtifact:
    return build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(
                ingestion_id=ingestion_id,
            ),
        ),
    )


def write_artifact(
    tmp_path: Path,
    *,
    artifact: KnowledgeIngestionRegistryArtifact | None = None,
) -> tuple[
    KnowledgeIngestionRegistryStorageLocation,
    KnowledgeIngestionRegistryArtifact,
]:
    location = create_location(
        tmp_path,
    )
    selected = (
        artifact
        if artifact is not None
        else create_artifact()
    )
    write_knowledge_ingestion_registry_artifact(
        location=location,
        artifact=selected,
    )
    return location, selected


def failure_result(
    tmp_path: Path,
    *,
    status: KnowledgeIngestionRegistryRecoveryStatus,
    failure_type: str = "Failure",
    failure_detail: str = "failure detail",
) -> KnowledgeIngestionRegistryRecoveryResult:
    return KnowledgeIngestionRegistryRecoveryResult(
        status=status,
        artifact_path=create_location(tmp_path).artifact_path,
        artifact=None,
        failure_type=failure_type,
        failure_detail=failure_detail,
    )


def test_recovery_status_vocabulary_is_exact() -> None:
    assert tuple(
        status.value
        for status in KnowledgeIngestionRegistryRecoveryStatus
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
            KnowledgeIngestionRegistryRecoveryStatus.INVALID_ENCODING,
            KnowledgeIngestionRegistryRecoveryStatus.MALFORMED_STORAGE,
            KnowledgeIngestionRegistryRecoveryStatus.INVALID_STRUCTURE,
            KnowledgeIngestionRegistryRecoveryStatus.INTEGRITY_MISMATCH,
            KnowledgeIngestionRegistryRecoveryStatus.NONCANONICAL_STORAGE,
            KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
        )
    )


def test_recovery_result_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeIngestionRegistryRecoveryResult
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
        status=KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
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
        match="KnowledgeIngestionRegistryRecoveryStatus",
    ):
        KnowledgeIngestionRegistryRecoveryResult(
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND,
            artifact_path="/registry/primary.registry.json",
            artifact=None,
            failure_type=None,
            failure_detail=None,
        )


def test_recovery_result_rejects_relative_path() -> None:
    with pytest.raises(
        ValueError,
        match="artifact_path must be absolute",
    ):
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND,
            artifact_path=Path("primary.registry.json"),
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.RECOVERED,
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.RECOVERED,
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND,
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND,
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
    status: KnowledgeIngestionRegistryRecoveryStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="non-recovered status",
    ):
        KnowledgeIngestionRegistryRecoveryResult(
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
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
        KnowledgeIngestionRegistryRecoveryResult(
            status=KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE,
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.RECOVERED
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.NOT_FOUND
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.INVALID_ENCODING
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.MALFORMED_STORAGE
    )
    assert result.failure_type == "MalformedRegistryStorageError"
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.INVALID_STRUCTURE
    )
    assert result.failure_type == (
        "InvalidRegistryStorageStructureError"
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.INTEGRITY_MISMATCH
    )
    assert result.failure_type == (
        "RegistryStorageIntegrityMismatchError"
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
    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.NONCANONICAL_STORAGE
    )
    assert result.failure_type == "NoncanonicalRegistryStorageError"
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

    result = recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert result.status is (
        KnowledgeIngestionRegistryRecoveryStatus.IO_FAILURE
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
    recover_knowledge_ingestion_registry_artifact(
        location=location,
    )
    assert not location.storage_root.exists()


def test_recovery_result_grants_no_repair_or_authority_claim() -> None:
    names = {
        field.name
        for field in fields(
            KnowledgeIngestionRegistryRecoveryResult
        )
    }
    assert "repaired" not in names
    assert "authentic" not in names
    assert "authoritative" not in names
    assert "truth" not in names
