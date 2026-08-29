import json

import pytest

from sp001.services.knowledge_ingestion_registry_payload_validation import (
    validate_knowledge_ingestion_registry_payload,
)
from sp001.services.knowledge_ingestion_registry_serialization import (
    serialize_knowledge_ingestion_registry,
)
from test_knowledge_ingestion_registry_serialization import (
    create_record,
    create_registry,
)


def create_payload() -> str:
    return serialize_knowledge_ingestion_registry(
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


def test_valid_canonical_registry_payload_passes() -> None:
    assert validate_knowledge_ingestion_registry_payload(
        payload=create_payload(),
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
def test_non_string_payload_is_rejected(
    invalid_payload: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="payload must be a string",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=invalid_payload,
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
def test_empty_payload_is_rejected(
    empty_payload: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="payload must not be empty",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=empty_payload,
        )


def test_malformed_json_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="valid JSON",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload="{",
        )


@pytest.mark.parametrize(
    "document",
    (
        [],
        None,
        "registry",
        1,
    ),
)
def test_non_object_root_is_rejected(
    document: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="JSON object",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "missing_field",
    (
        "records",
        "schema_version",
    ),
)
def test_missing_root_field_is_rejected(
    missing_field: str,
) -> None:
    document = json.loads(
        create_payload(),
    )

    del document[
        missing_field
    ]

    with pytest.raises(
        ValueError,
        match="missing required registry fields",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_unexpected_root_field_is_rejected() -> None:
    document = json.loads(
        create_payload(),
    )

    document["authority"] = "UNSUPPORTED"

    with pytest.raises(
        ValueError,
        match="unexpected registry fields",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
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
def test_invalid_schema_version_is_rejected(
    invalid_version: object,
) -> None:
    document = json.loads(
        create_payload(),
    )

    document["schema_version"] = invalid_version

    with pytest.raises(
        ValueError,
        match="supported version 1",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_records_must_be_array() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"] = {}

    with pytest.raises(
        ValueError,
        match="records must be a JSON array",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_record_must_be_object() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0] = []

    with pytest.raises(
        ValueError,
        match="registry record must be a JSON object",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "missing_field",
    (
        "artifact",
        "fragments",
        "ingestion_id",
    ),
)
def test_missing_record_field_is_rejected(
    missing_field: str,
) -> None:
    document = json.loads(
        create_payload(),
    )

    del document["records"][0][
        missing_field
    ]

    with pytest.raises(
        ValueError,
        match="missing required registry record fields",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_empty_ingestion_identity_is_rejected() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["ingestion_id"] = " "

    with pytest.raises(
        ValueError,
        match="ingestion_id must not be empty",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_duplicate_ingestion_identity_is_rejected() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"].append(
        document["records"][0],
    )

    with pytest.raises(
        ValueError,
        match="ingestion_id must be unique",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "artifact_value",
    (
        None,
        [],
        "artifact",
    ),
)
def test_artifact_must_be_object(
    artifact_value: object,
) -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["artifact"] = artifact_value

    with pytest.raises(
        ValueError,
        match="artifact must be a JSON object",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_missing_artifact_field_is_rejected() -> None:
    document = json.loads(
        create_payload(),
    )

    del document["records"][0]["artifact"][
        "source"
    ]

    with pytest.raises(
        ValueError,
        match="missing required artifact fields",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    (
        "container",
        "field",
    ),
    (
        (
            "source",
            "source_id",
        ),
        (
            "source",
            "source_version",
        ),
        (
            "extraction",
            "extraction_id",
        ),
        (
            "extraction",
            "extractor_id",
        ),
        (
            "extraction",
            "extractor_version",
        ),
    ),
)
def test_nested_identity_must_not_be_empty(
    container: str,
    field: str,
) -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["artifact"][
        container
    ][field] = ""

    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


@pytest.mark.parametrize(
    "digest_path",
    (
        (
            "artifact",
            "content_digest",
        ),
        (
            "artifact",
            "source",
            "content_digest",
        ),
        (
            "artifact",
            "extraction",
            "configuration_digest",
        ),
        (
            "fragments",
            0,
            "content_digest",
        ),
    ),
)
def test_invalid_nested_digest_is_rejected(
    digest_path: tuple,
) -> None:
    document = json.loads(
        create_payload(),
    )

    target = document[
        "records"
    ][0]

    for component in digest_path:
        target = target[
            component
        ]

    target["value"] = "INVALID"

    with pytest.raises(
        ValueError,
        match="64 lowercase hexadecimal characters",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_fragments_must_be_array() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["fragments"] = {}

    with pytest.raises(
        ValueError,
        match="fragments must be a JSON array",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_fragment_must_be_object() -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["fragments"][0] = []

    with pytest.raises(
        ValueError,
        match="fragment must be a JSON object",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
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
            "sequence_number",
            -1,
            "non-negative integer",
        ),
        (
            "sequence_number",
            True,
            "non-negative integer",
        ),
        (
            "byte_start",
            -1,
            "non-negative integer",
        ),
        (
            "byte_start",
            True,
            "non-negative integer",
        ),
        (
            "byte_end",
            0,
            "positive integer",
        ),
    ),
)
def test_invalid_fragment_number_is_rejected(
    field: str,
    invalid_value: object,
    message: str,
) -> None:
    document = json.loads(
        create_payload(),
    )

    document["records"][0]["fragments"][0][
        field
    ] = invalid_value

    with pytest.raises(
        ValueError,
        match=message,
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_invalid_half_open_fragment_range_is_rejected() -> None:
    document = json.loads(
        create_payload(),
    )

    fragment = document[
        "records"
    ][0]["fragments"][0]

    fragment["byte_start"] = 1
    fragment["byte_end"] = 1

    with pytest.raises(
        ValueError,
        match="byte_end must be greater than byte_start",
    ):
        validate_knowledge_ingestion_registry_payload(
            payload=encode(
                document,
            ),
        )


def test_validation_requires_no_digest_or_authenticity() -> None:
    payload = create_payload()

    assert validate_knowledge_ingestion_registry_payload(
        payload=payload,
    )

    assert "signature" not in payload
    assert "authenticity" not in payload
    assert "authority" not in payload
