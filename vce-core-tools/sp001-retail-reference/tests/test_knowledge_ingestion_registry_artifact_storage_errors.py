from dataclasses import replace
import hashlib
import json

import pytest

from sp001.services.knowledge_ingestion_registry_artifact import (
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_deserialization import (
    InvalidRegistryStorageStructureError,
    KnowledgeIngestionRegistryStorageError,
    MalformedRegistryStorageError,
    NoncanonicalRegistryStorageError,
    RegistryStorageIntegrityMismatchError,
    deserialize_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_serialization import (
    serialize_knowledge_ingestion_registry_artifact,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def create_artifact():
    return build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(),
        ),
    )


def encode(document: object) -> str:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def canonical_document() -> dict:
    return json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        )
    )


def test_storage_errors_remain_value_errors() -> None:
    for error_type in (
        KnowledgeIngestionRegistryStorageError,
        MalformedRegistryStorageError,
        InvalidRegistryStorageStructureError,
        RegistryStorageIntegrityMismatchError,
        NoncanonicalRegistryStorageError,
    ):
        assert issubclass(
            error_type,
            ValueError,
        )


@pytest.mark.parametrize(
    "stored_artifact",
    (
        "",
        " ",
        "\n\t",
        "{",
        '{"payload":',
    ),
)
def test_empty_or_invalid_json_is_malformed(
    stored_artifact: str,
) -> None:
    with pytest.raises(
        MalformedRegistryStorageError,
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored_artifact,
        )


@pytest.mark.parametrize(
    "document",
    (
        None,
        [],
        "artifact",
        1,
    ),
)
def test_non_object_root_has_invalid_structure(
    document: object,
) -> None:
    with pytest.raises(
        InvalidRegistryStorageStructureError,
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_missing_envelope_field_has_invalid_structure() -> None:
    document = canonical_document()
    del document["digest"]

    with pytest.raises(
        InvalidRegistryStorageStructureError,
        match="missing required storage envelope fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_duplicate_field_has_invalid_structure() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )
    duplicated = stored.replace(
        "{",
        '{"media_type":"duplicate",',
        1,
    )

    with pytest.raises(
        InvalidRegistryStorageStructureError,
        match="duplicate JSON field",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=duplicated,
        )


def test_invalid_digest_metadata_has_invalid_structure() -> None:
    document = canonical_document()
    document["digest"]["algorithm"] = "MD5"

    with pytest.raises(
        InvalidRegistryStorageStructureError,
        match="digest algorithm must be SHA-256",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_matching_digest_cannot_validate_invalid_payload_structure() -> None:
    document = canonical_document()
    document["payload"] = "{}"
    document["digest"]["value"] = hashlib.sha256(
        b"{}"
    ).hexdigest()

    with pytest.raises(
        InvalidRegistryStorageStructureError,
        match="missing required registry fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_digest_mismatch_has_explicit_integrity_error() -> None:
    document = canonical_document()
    document["digest"]["value"] = "0" * 64

    with pytest.raises(
        RegistryStorageIntegrityMismatchError,
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_noncanonical_json_has_explicit_error() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    with pytest.raises(
        NoncanonicalRegistryStorageError,
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact="\n" + stored,
        )


def test_valid_canonical_artifact_is_unchanged() -> None:
    artifact = create_artifact()
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored,
        )
        == artifact
    )


def test_error_types_grant_no_repair_or_authenticity_claim() -> None:
    names = {
        error_type.__name__.lower()
        for error_type in (
            KnowledgeIngestionRegistryStorageError,
            MalformedRegistryStorageError,
            InvalidRegistryStorageStructureError,
            RegistryStorageIntegrityMismatchError,
            NoncanonicalRegistryStorageError,
        )
    }

    assert all(
        "repair" not in name
        for name in names
    )
    assert all(
        "authentic" not in name
        for name in names
    )
