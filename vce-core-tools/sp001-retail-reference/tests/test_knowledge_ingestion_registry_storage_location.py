from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from sp001.contracts.knowledge_ingestion_registry_storage_location import (
    KNOWLEDGE_INGESTION_REGISTRY_FILE_SUFFIX,
    MAXIMUM_STORAGE_LOGICAL_NAME_LENGTH,
    KnowledgeIngestionRegistryStorageLocation,
)


def create_location(
    tmp_path: Path,
    *,
    logical_name: str = "primary",
) -> KnowledgeIngestionRegistryStorageLocation:
    return KnowledgeIngestionRegistryStorageLocation(
        storage_root=tmp_path / "registry-storage",
        logical_name=logical_name,
    )


def test_location_is_immutable(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        location.logical_name = "changed"


def test_location_preserves_absolute_storage_root(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    assert location.storage_root.is_absolute()

    assert location.storage_root == (
        tmp_path / "registry-storage"
    )


def test_location_builds_fixed_registry_artifact_path(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
        logical_name="customer-mx",
    )

    assert location.artifact_path == (
        tmp_path
        / "registry-storage"
        / "customer-mx.registry.json"
    )

    assert (
        location.artifact_path.suffixes
        == [
            ".registry",
            ".json",
        ]
    )

    assert (
        KNOWLEDGE_INGESTION_REGISTRY_FILE_SUFFIX
        == ".registry.json"
    )


def test_location_resolution_is_deterministic(
    tmp_path: Path,
) -> None:
    first = create_location(
        tmp_path,
    )

    second = create_location(
        tmp_path,
    )

    assert first == second
    assert first.artifact_path == second.artifact_path


def test_distinct_logical_names_produce_distinct_paths(
    tmp_path: Path,
) -> None:
    first = create_location(
        tmp_path,
        logical_name="customer-a",
    )

    second = create_location(
        tmp_path,
        logical_name="customer-b",
    )

    assert first.artifact_path != second.artifact_path


@pytest.mark.parametrize(
    "invalid_root",
    (
        None,
        "/tmp/storage",
        {},
        (),
    ),
)
def test_location_rejects_untyped_storage_root(
    invalid_root: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="storage_root must be a Path",
    ):
        KnowledgeIngestionRegistryStorageLocation(
            storage_root=invalid_root,
            logical_name="primary",
        )


def test_location_rejects_relative_storage_root() -> None:
    with pytest.raises(
        ValueError,
        match="storage_root must be absolute",
    ):
        KnowledgeIngestionRegistryStorageLocation(
            storage_root=Path(
                "relative-storage",
            ),
            logical_name="primary",
        )


def test_location_rejects_filesystem_root() -> None:
    root = Path(
        "/",
    )

    with pytest.raises(
        ValueError,
        match="must not be a filesystem root",
    ):
        KnowledgeIngestionRegistryStorageLocation(
            storage_root=root,
            logical_name="primary",
        )


@pytest.mark.parametrize(
    "invalid_name",
    (
        None,
        {},
        (),
        b"primary",
    ),
)
def test_location_rejects_untyped_logical_name(
    tmp_path: Path,
    invalid_name: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="logical_name must be a string",
    ):
        KnowledgeIngestionRegistryStorageLocation(
            storage_root=tmp_path,
            logical_name=invalid_name,
        )


def test_location_rejects_empty_logical_name(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        ValueError,
        match="logical_name must not be empty",
    ):
        create_location(
            tmp_path,
            logical_name="",
        )


@pytest.mark.parametrize(
    "reserved_name",
    (
        ".",
        "..",
    ),
)
def test_location_rejects_reserved_path_component(
    tmp_path: Path,
    reserved_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="reserved path component",
    ):
        create_location(
            tmp_path,
            logical_name=reserved_name,
        )


@pytest.mark.parametrize(
    "traversal_name",
    (
        "../escape",
        "folder/name",
        r"folder\name",
        "/absolute",
        r"C:\absolute",
        "~/registry",
    ),
)
def test_location_rejects_path_traversal_or_separator(
    tmp_path: Path,
    traversal_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="only ASCII letters",
    ):
        create_location(
            tmp_path,
            logical_name=traversal_name,
        )


@pytest.mark.parametrize(
    "invalid_name",
    (
        " primary",
        "primary ",
        "primary registry",
        ".hidden",
        "~primary",
    ),
)
def test_location_rejects_unsupported_name_characters(
    tmp_path: Path,
    invalid_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="only ASCII letters",
    ):
        create_location(
            tmp_path,
            logical_name=invalid_name,
        )


def test_location_accepts_maximum_name_length(
    tmp_path: Path,
) -> None:
    name = "a" * MAXIMUM_STORAGE_LOGICAL_NAME_LENGTH

    location = create_location(
        tmp_path,
        logical_name=name,
    )

    assert location.logical_name == name


def test_location_rejects_name_above_maximum_length(
    tmp_path: Path,
) -> None:
    name = "a" * (
        MAXIMUM_STORAGE_LOGICAL_NAME_LENGTH
        + 1
    )

    with pytest.raises(
        ValueError,
        match="at most 128 characters",
    ):
        create_location(
            tmp_path,
            logical_name=name,
        )


def test_location_creation_does_not_touch_filesystem(
    tmp_path: Path,
) -> None:
    storage_root = (
        tmp_path
        / "missing-storage"
    )

    location = (
        KnowledgeIngestionRegistryStorageLocation(
            storage_root=storage_root,
            logical_name="primary",
        )
    )

    assert not storage_root.exists()
    assert not location.artifact_path.exists()


def test_location_grants_no_storage_or_authority_capability(
    tmp_path: Path,
) -> None:
    location = create_location(
        tmp_path,
    )

    for attribute in (
        "write",
        "read",
        "delete",
        "replace",
        "persist",
        "authority",
        "approved",
        "signature",
        "authenticity",
    ):
        assert not hasattr(
            location,
            attribute,
        )
