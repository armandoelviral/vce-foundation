from dataclasses import replace
import hashlib
import json

import pytest

from sp001.services.knowledge_ingestion_registry_artifact import (
    KnowledgeIngestionRegistryArtifact,
    build_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_deserialization import (
    deserialize_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_artifact_storage_serialization import (
    serialize_knowledge_ingestion_registry_artifact,
)
from sp001.services.knowledge_ingestion_registry_digest import (
    KnowledgeIngestionRegistryDigest,
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


def test_storage_round_trip_preserves_artifact() -> None:
    artifact = create_artifact()

    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=artifact,
    )

    recovered = (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored,
        )
    )

    assert recovered == artifact


def test_storage_round_trip_preserves_unicode() -> None:
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

    recovered = (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored,
        )
    )

    assert recovered == artifact
    assert "INGESTIÓN-Ñ" in recovered.payload


def test_deserialization_returns_artifact_not_registry() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    recovered = (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored,
        )
    )

    assert isinstance(
        recovered,
        KnowledgeIngestionRegistryArtifact,
    )

    assert not hasattr(
        recovered,
        "records",
    )


@pytest.mark.parametrize(
    "invalid_stored_artifact",
    (
        None,
        {},
        (),
        b"{}",
    ),
)
def test_deserialization_rejects_non_text_input(
    invalid_stored_artifact: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="stored_artifact must be a string",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=invalid_stored_artifact,
        )


@pytest.mark.parametrize(
    "empty_stored_artifact",
    (
        "",
        " ",
        "\n",
        "\t",
    ),
)
def test_deserialization_rejects_empty_input(
    empty_stored_artifact: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="stored_artifact must not be empty",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=empty_stored_artifact,
        )


def test_deserialization_rejects_malformed_json() -> None:
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact="{",
        )


@pytest.mark.parametrize(
    "document",
    (
        [],
        None,
        "artifact",
        1,
    ),
)
def test_deserialization_rejects_non_object_root(
    document: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="JSON object",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "missing_field",
    (
        "digest",
        "media_type",
        "payload",
        "schema_version",
    ),
)
def test_deserialization_rejects_missing_envelope_field(
    missing_field: str,
) -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    del document[
        missing_field
    ]

    with pytest.raises(
        ValueError,
        match="missing required storage envelope fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_deserialization_rejects_unexpected_envelope_field() -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    document["authority"] = "UNSUPPORTED"

    with pytest.raises(
        ValueError,
        match="unexpected storage envelope fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "invalid_digest",
    (
        None,
        [],
        "digest",
    ),
)
def test_deserialization_rejects_non_object_digest(
    invalid_digest: object,
) -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    document["digest"] = invalid_digest

    with pytest.raises(
        ValueError,
        match="stored digest must be a JSON object",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "missing_field",
    (
        "algorithm",
        "encoding",
        "value",
    ),
)
def test_deserialization_rejects_missing_digest_field(
    missing_field: str,
) -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    del document["digest"][
        missing_field
    ]

    with pytest.raises(
        ValueError,
        match="missing required stored digest fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_deserialization_rejects_unexpected_digest_field() -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    document["digest"]["signature"] = "UNSUPPORTED"

    with pytest.raises(
        ValueError,
        match="unexpected stored digest fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    (
        "field",
        "invalid_value",
        "message",
    ),
    (
        (
            "algorithm",
            "SHA-512",
            "algorithm must be SHA-256",
        ),
        (
            "encoding",
            "UTF-16",
            "encoding must be UTF-8",
        ),
        (
            "value",
            "0" * 63,
            "64 lowercase hexadecimal characters",
        ),
    ),
)
def test_deserialization_rejects_invalid_digest_metadata(
    field: str,
    invalid_value: object,
    message: str,
) -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    document["digest"][
        field
    ] = invalid_value

    with pytest.raises(
        ValueError,
        match=message,
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_deserialization_rejects_payload_digest_mismatch() -> None:
    document = json.loads(
        serialize_knowledge_ingestion_registry_artifact(
            artifact=create_artifact(),
        ),
    )

    document["payload"] = (
        document["payload"]
        + " "
    )

    with pytest.raises(
        ValueError,
        match="integrity verification failed",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_matching_digest_cannot_validate_invalid_payload_structure() -> None:
    payload = "{}"

    document = {
        "digest": {
            "algorithm": "SHA-256",
            "encoding": "UTF-8",
            "value": hashlib.sha256(
                payload.encode(
                    "utf-8",
                )
            ).hexdigest(),
        },
        "media_type": "application/json",
        "payload": payload,
        "schema_version": 1,
    }

    with pytest.raises(
        ValueError,
        match="missing required registry fields",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=encode(
                document,
            ),
        )


def test_deserialization_rejects_noncanonical_storage_json() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    with pytest.raises(
        ValueError,
        match="canonical JSON",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored + "\n",
        )


def test_deserialization_rejects_duplicate_json_field() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    duplicated = stored.replace(
        "{",
        '{"media_type":"duplicate",',
        1,
    )

    with pytest.raises(
        ValueError,
        match="duplicate JSON field: media_type",
    ):
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=duplicated,
        )


def test_recovered_artifact_claims_no_authenticity() -> None:
    stored = serialize_knowledge_ingestion_registry_artifact(
        artifact=create_artifact(),
    )

    recovered = (
        deserialize_knowledge_ingestion_registry_artifact(
            stored_artifact=stored,
        )
    )

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "customer_acceptance",
    ):
        assert not hasattr(
            recovered,
            attribute,
        )
