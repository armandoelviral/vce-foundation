from dataclasses import replace
import json

import pytest

from sp001.services.knowledge_ingestion_registry_artifact import (
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_serialization import (
    serialize_knowledge_ingestion_registry_artifact,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def create_artifact(
    *,
    ingestion_id: str = "INGESTION-001",
):
    return build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(
                ingestion_id=ingestion_id,
            ),
        ),
    )


def test_storage_serializer_returns_text() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    assert isinstance(
        stored,
        str,
    )


def test_storage_envelope_has_exact_root_fields() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    document = json.loads(
        stored,
    )

    assert set(
        document,
    ) == {
        "digest",
        "media_type",
        "payload",
        "schema_version",
    }


def test_storage_envelope_preserves_exact_payload() -> None:
    artifact = create_artifact()

    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        ),
    )

    assert document["payload"] == artifact.payload


def test_storage_envelope_preserves_complete_digest() -> None:
    artifact = create_artifact()

    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        ),
    )

    assert document["digest"] == {
        "algorithm": artifact.digest.algorithm,
        "encoding": artifact.digest.encoding,
        "value": artifact.digest.value,
    }


def test_storage_envelope_preserves_media_type() -> None:
    artifact = create_artifact()

    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        ),
    )

    assert document["media_type"] == artifact.media_type


def test_storage_envelope_preserves_external_schema_version() -> None:
    artifact = create_artifact()

    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=artifact,
        ),
    )

    assert (
        document["schema_version"]
        == artifact.schema_version
        == 1
    )


def test_storage_serialization_is_deterministic() -> None:
    first = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    second = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    assert first == second


def test_storage_serialization_uses_compact_json() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    assert ": " not in stored
    assert ", " not in stored
    assert "\n" not in stored


def test_storage_serialization_preserves_unicode() -> None:
    artifact = build_knowledge_ingestion_registry_artifact(
        registry=create_registry(
            create_record(
                ingestion_id="INGESTIÓN-Ñ",
                artifact_id="ARTEFACTO-CAFÉ",
                source_id="FUENTE-NIÑEZ",
            ),
        ),
    )

    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert "INGESTIÓN-Ñ" in stored
    assert "ARTEFACTO-CAFÉ" in stored
    assert "FUENTE-NIÑEZ" in stored


@pytest.mark.parametrize(
    "invalid_artifact",
    (
        None,
        {},
        (),
        "artifact",
    ),
)
def test_storage_serialization_rejects_untyped_artifact(
    invalid_artifact: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeIngestionRegistryArtifact",
    ):
        serialize_knowledge_ingestion_registry_artifact(
            artifact=invalid_artifact,
        )


def test_storage_serialization_blocks_digest_mismatch() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        payload=artifact.payload + " ",
    )

    with pytest.raises(
        ValueError,
        match="integrity verification failed",
    ):
        serialize_knowledge_ingestion_registry_artifact(
            artifact=modified,
        )


def test_storage_serialization_blocks_invalid_structure() -> None:
    artifact = create_artifact()

    modified = replace(
        artifact,
        payload="{}",
        digest=replace(
            artifact.digest,
            value=(
                "44136fa355b3678a1146ad16f7e8649e"
                "94fb4fc21fe77e8310c060f61caaff8a"
            ),
        ),
    )

    with pytest.raises(
        ValueError,
        match="missing required registry fields",
    ):
        serialize_knowledge_ingestion_registry_artifact(
            artifact=modified,
        )


def test_storage_serialization_does_not_mutate_artifact() -> None:
    artifact = create_artifact()

    before = artifact

    serialize_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    assert artifact == before


def test_storage_envelope_claims_no_authenticity() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    document = json.loads(
        stored,
    )

    assert "signature" not in document
    assert "signer" not in document
    assert "authenticity" not in document
    assert "authority" not in document
