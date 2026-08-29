from dataclasses import replace
import hashlib

import pytest

from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_verification import (
    verify_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def create_artifact() -> KnowledgeIngestionRegistryArtifact:
    return build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(),
        ),
    )


def digest_for(
    payload: str,
) -> KnowledgeIngestionRegistryDigest:
    return KnowledgeIngestionRegistryDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=hashlib.sha256(
            payload.encode(
                "utf-8",
            )
        ).hexdigest(),
    )


def test_valid_registry_artifact_passes_verification() -> None:
    assert verify_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )


def test_verification_requires_no_original_registry() -> None:
    artifact = create_artifact()

    result = verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert result is True


def test_modified_payload_is_rejected() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        payload=artifact.payload.replace(
            "INGESTION-001",
            "INGESTION-CHANGED",
        ),
    )

    assert not verify_knowledge_ingestion_registry_artifact(
        artifact=modified,
    )


def test_modified_json_formatting_is_rejected() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        payload=artifact.payload + " ",
    )

    assert not verify_knowledge_ingestion_registry_artifact(
        artifact=modified,
    )


def test_modified_digest_value_is_rejected() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        digest=replace(
            artifact.digest,
            value="0" * 64,
        ),
    )

    assert not verify_knowledge_ingestion_registry_artifact(
        artifact=modified,
    )


@pytest.mark.parametrize(
    "invalid_artifact",
    (
        None,
        {},
        (),
        "artifact",
    ),
)
def test_verification_rejects_untyped_artifact(
    invalid_artifact: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistryArtifact",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=invalid_artifact,
        )


def test_verification_rejects_unsupported_media_type() -> None:
    artifact = replace(
        create_artifact(),
        media_type="text/plain",
    )

    with pytest.raises(
        ValueError,
        match="media_type must be application/json",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "invalid_version",
    (
        None,
        True,
        0,
        2,
        "1",
    ),
)
def test_verification_rejects_invalid_schema_version(
    invalid_version: object,
) -> None:
    artifact = replace(
        create_artifact(),
        schema_version=invalid_version,
    )

    with pytest.raises(
        ValueError,
        match="supported version 1",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "invalid_payload",
    (
        None,
        {},
        (),
        b"{}",
    ),
)
def test_verification_rejects_non_text_payload(
    invalid_payload: object,
) -> None:
    artifact = replace(
        create_artifact(),
        payload=invalid_payload,
    )

    with pytest.raises(
        TypeError,
        match="payload must be a string",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "empty_payload",
    (
        "",
        " ",
        "\n",
        "\t",
    ),
)
def test_verification_rejects_empty_payload(
    empty_payload: str,
) -> None:
    artifact = replace(
        create_artifact(),
        payload=empty_payload,
    )

    with pytest.raises(
        ValueError,
        match="payload must not be empty",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


def test_verification_rejects_untyped_digest() -> None:
    artifact = replace(
        create_artifact(),
        digest=None,
    )

    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistryDigest",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


def test_verification_rejects_unsupported_digest_algorithm() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        digest=replace(
            artifact.digest,
            algorithm="SHA-512",
        ),
    )

    with pytest.raises(
        ValueError,
        match="algorithm must be SHA-256",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=modified,
        )


def test_verification_rejects_unsupported_digest_encoding() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        digest=replace(
            artifact.digest,
            encoding="UTF-16",
        ),
    )

    with pytest.raises(
        ValueError,
        match="encoding must be UTF-8",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=modified,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        "",
        "0" * 63,
        "0" * 65,
        "G" * 64,
        "A" * 64,
        123,
    ),
)
def test_verification_rejects_invalid_digest_format(
    invalid_value: object,
) -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        digest=replace(
            artifact.digest,
            value=invalid_value,
        ),
    )

    with pytest.raises(
        ValueError,
        match="64 lowercase hexadecimal characters",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=modified,
        )


def test_matching_digest_cannot_validate_invalid_structure() -> None:
    payload = "{}"

    artifact = KnowledgeIngestionRegistryArtifact(
        payload=payload,
        digest=digest_for(
            payload,
        ),
        media_type="application/json",
        schema_version=1,
    )

    with pytest.raises(
        ValueError,
        match="missing required registry fields",
    ):
        verify_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        )


def test_digest_mismatch_returns_false_before_structure_validation() -> None:
    original = create_artifact()

    artifact = replace(
        original,
        payload="{}",
    )

    assert not verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )


def test_verification_hashes_exact_received_utf8_payload() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(
                ingestion_id="INGESTIÓN-Ñ",
                artifact_id="ARTEFACTO-CAFÉ",
                source_id="FUENTE-NIÑEZ",
            ),
        ),
    )

    assert verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    modified = replace(
        artifact,
        payload=artifact.payload.replace(
            "CAFÉ",
            "CAFE",
        ),
    )

    assert not verify_knowledge_ingestion_registry_artifact(
        artifact=modified,
    )


def test_verification_does_not_mutate_artifact() -> None:
    artifact = create_artifact()

    before = artifact

    verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert artifact == before


def test_success_claims_neither_authenticity_nor_authority() -> None:
    artifact = create_artifact()

    result = verify_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert result is True

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            artifact,
            attribute,
        )
