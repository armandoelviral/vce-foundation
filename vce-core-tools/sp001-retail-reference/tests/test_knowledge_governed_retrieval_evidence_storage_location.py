import ast

from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

import sp001.contracts.knowledge_governed_retrieval_evidence_storage_location as location_module
from sp001.contracts.knowledge_governed_retrieval_evidence_storage_location import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_FILE_SUFFIX,
    MAXIMUM_RETRIEVAL_EVIDENCE_STORAGE_LOGICAL_NAME_LENGTH,
    KnowledgeGovernedRetrievalEvidenceStorageLocation,
)


def create_location(
    storage_root: Path,
    logical_name: str = "retrieval-run-001",
) -> KnowledgeGovernedRetrievalEvidenceStorageLocation:
    return KnowledgeGovernedRetrievalEvidenceStorageLocation(
        storage_root=storage_root,
        logical_name=logical_name,
    )


def test_location_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceStorageLocation
        )
    ) == (
        "storage_root",
        "logical_name",
    )


def test_location_is_immutable(tmp_path: Path) -> None:
    location = create_location(tmp_path)
    with pytest.raises(FrozenInstanceError):
        location.logical_name = "changed"


def test_location_preserves_absolute_storage_root(tmp_path: Path) -> None:
    location = create_location(tmp_path)
    assert location.storage_root is tmp_path
    assert location.storage_root.is_absolute()


def test_location_builds_fixed_evidence_artifact_path(tmp_path: Path) -> None:
    location = create_location(tmp_path)
    assert KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_FILE_SUFFIX == (
        ".retrieval-evidence.json"
    )
    assert location.artifact_path == (
        tmp_path / "retrieval-run-001.retrieval-evidence.json"
    )
    assert location.artifact_path.parent == tmp_path


def test_location_resolution_is_deterministic(tmp_path: Path) -> None:
    first = create_location(tmp_path)
    second = create_location(tmp_path)
    assert first == second
    assert first.artifact_path == second.artifact_path


def test_distinct_logical_names_produce_distinct_paths(tmp_path: Path) -> None:
    first = create_location(tmp_path, "retrieval-run-001")
    second = create_location(tmp_path, "retrieval-run-002")
    assert first.artifact_path != second.artifact_path


@pytest.mark.parametrize("storage_root", (None, "tmp", b"tmp", object()))
def test_location_rejects_untyped_storage_root(storage_root: object) -> None:
    with pytest.raises(TypeError, match="storage_root must be a Path"):
        create_location(storage_root)


def test_location_rejects_relative_storage_root() -> None:
    with pytest.raises(ValueError, match="must be absolute"):
        create_location(Path("relative/storage"))


def test_location_rejects_filesystem_root() -> None:
    with pytest.raises(ValueError, match="filesystem root"):
        create_location(Path("/"))


@pytest.mark.parametrize("logical_name", (None, 1, b"name", object()))
def test_location_rejects_untyped_logical_name(
    tmp_path: Path,
    logical_name: object,
) -> None:
    with pytest.raises(TypeError, match="logical_name must be a string"):
        create_location(tmp_path, logical_name)


def test_location_rejects_empty_logical_name(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        create_location(tmp_path, "")


@pytest.mark.parametrize("logical_name", (".", ".."))
def test_location_rejects_reserved_path_component(
    tmp_path: Path,
    logical_name: str,
) -> None:
    with pytest.raises(ValueError, match="reserved path component"):
        create_location(tmp_path, logical_name)


@pytest.mark.parametrize(
    "logical_name",
    (
        "../escape",
        "nested/file",
        "nested\\file",
        "/absolute",
        "C:\\absolute",
    ),
)
def test_location_rejects_traversal_or_separator(
    tmp_path: Path,
    logical_name: str,
) -> None:
    with pytest.raises(ValueError, match="only ASCII letters"):
        create_location(tmp_path, logical_name)


@pytest.mark.parametrize(
    "logical_name",
    (
        " leading",
        "-leading",
        "_leading",
        ".hidden",
        "contains space",
        "evidencia-á",
        "name.json?query",
    ),
)
def test_location_rejects_unsupported_name_characters(
    tmp_path: Path,
    logical_name: str,
) -> None:
    with pytest.raises(ValueError, match="only ASCII letters"):
        create_location(tmp_path, logical_name)


def test_location_accepts_maximum_logical_name_length(tmp_path: Path) -> None:
    logical_name = (
        "a"
        * MAXIMUM_RETRIEVAL_EVIDENCE_STORAGE_LOGICAL_NAME_LENGTH
    )
    location = create_location(tmp_path, logical_name)
    assert location.logical_name == logical_name


def test_location_rejects_name_above_maximum_length(tmp_path: Path) -> None:
    logical_name = "a" * (
        MAXIMUM_RETRIEVAL_EVIDENCE_STORAGE_LOGICAL_NAME_LENGTH + 1
    )
    with pytest.raises(ValueError, match="at most 128 characters"):
        create_location(tmp_path, logical_name)


def test_location_creation_does_not_touch_filesystem(tmp_path: Path) -> None:
    storage_root = tmp_path / "absent" / "evidence"
    location = create_location(storage_root)
    assert not storage_root.exists()
    assert not location.artifact_path.exists()


def test_location_grants_no_storage_transport_or_authority_capability() -> None:
    source = Path(location_module.__file__).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    called_attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
    }
    assert not {
        "mkdir",
        "open",
        "read_text",
        "read_bytes",
        "write_text",
        "write_bytes",
        "replace",
        "rename",
        "unlink",
        "remove",
        "rmdir",
    } & called_attributes
    assert "http" not in source.casefold()
    assert "authority" not in source.casefold()
