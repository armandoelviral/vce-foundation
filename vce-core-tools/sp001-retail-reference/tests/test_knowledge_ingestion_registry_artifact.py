from dataclasses import FrozenInstanceError
import hashlib
import json

import pytest

from sp001.services.knowledge_ingestion_registry_artifact import (
    KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE,
    KnowledgeIngestionRegistryArtifact,
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
    digest_knowledge_ingestion_registry,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION,
    serialize_knowledge_ingestion_registry,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def test_builder_returns_immutable_registry_artifact() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    assert isinstance(
        artifact,
        KnowledgeIngestionRegistryArtifact,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        artifact.payload = "{}"


def test_artifact_contains_exact_canonical_payload() -> None:
    registry = create_registry(
        create_record(),
    )

    artifact = build_knowledge_ingestion_registry_artifact(
        registry=registry,
    )

    expected = serialize_knowledge_ingestion_registry(
        registry=registry,
    )

    assert artifact.payload == expected


def test_artifact_contains_registry_digest() -> None:
    registry = create_registry(
        create_record(),
    )

    artifact = build_knowledge_ingestion_registry_artifact(
        registry=registry,
    )

    expected = digest_knowledge_ingestion_registry(
        registry=registry,
    )

    assert isinstance(
        artifact.digest,
        KnowledgeIngestionRegistryDigest,
    )

    assert artifact.digest == expected


def test_artifact_digest_matches_exact_payload_bytes() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(),
        ),
    )

    expected = hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()

    assert artifact.digest.value == expected


def test_artifact_declares_json_media_type() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    assert (
        artifact.media_type
        == KNOWLEDGE_INGESTION_REGISTRY_MEDIA_TYPE
        == "application/json"
    )


def test_artifact_declares_registry_schema_version() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    assert (
        artifact.schema_version
        == KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION
        == 1
    )


def test_artifact_payload_embeds_same_schema_version() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    document = json.loads(
        artifact.payload,
    )

    assert (
        document["schema_version"]
        == artifact.schema_version
    )


def test_builder_supports_empty_registry() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    document = json.loads(
        artifact.payload,
    )

    assert document["records"] == []


def test_builder_preserves_declared_record_order() -> None:
    record_a = create_record(
        ingestion_id="INGESTION-A",
        artifact_id="ARTIFACT-A",
    )

    record_b = create_record(
        ingestion_id="INGESTION-B",
        artifact_id="ARTIFACT-B",
    )

    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            record_b,
            record_a,
        ),
    )

    document = json.loads(
        artifact.payload,
    )

    assert [
        record["ingestion_id"]
        for record in document["records"]
    ] == [
        "INGESTION-B",
        "INGESTION-A",
    ]


def test_builder_preserves_unicode_utf8_payload() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(
                ingestion_id="INGESTIÓN-Ñ",
                artifact_id="ARTEFACTO-CAFÉ",
                source_id="FUENTE-NIÑEZ",
            ),
        ),
    )

    assert "INGESTIÓN-Ñ" in artifact.payload
    assert "ARTEFACTO-CAFÉ" in artifact.payload
    assert "FUENTE-NIÑEZ" in artifact.payload

    assert artifact.digest.value == hashlib.sha256(
        artifact.payload.encode(
            "utf-8",
        )
    ).hexdigest()


def test_builder_is_deterministic_for_equivalent_registries() -> None:
    first = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(),
        ),
    )

    second = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(),
        ),
    )

    assert first == second


@pytest.mark.parametrize(
    "invalid_registry",
    (
        None,
        {},
        (),
        "registry",
    ),
)
def test_builder_rejects_untyped_registry(
    invalid_registry: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistry",
    ):
        build_knowledge_ingestion_registry_artifact(
            registry=invalid_registry,
        )


def test_builder_does_not_mutate_registry() -> None:
    registry = create_registry(
        create_record(),
    )

    records_before = registry.records

    build_knowledge_ingestion_registry_artifact(
        registry=registry,
    )

    assert registry.records == records_before


def test_artifact_makes_no_authenticity_or_authority_claim() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(),
    )

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "verified",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            artifact,
            attribute,
        )
