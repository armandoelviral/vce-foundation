import json
import re

from sp001.services.knowledge_ingestion_registry_serialization import (
    KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION,
)


ROOT_FIELDS = frozenset(
    (
        "records",
        "schema_version",
    )
)

RECORD_FIELDS = frozenset(
    (
        "artifact",
        "fragments",
        "ingestion_id",
    )
)

ARTIFACT_FIELDS = frozenset(
    (
        "artifact_id",
        "artifact_version",
        "content_digest",
        "extraction",
        "source",
    )
)

SOURCE_FIELDS = frozenset(
    (
        "content_digest",
        "source_id",
        "source_version",
    )
)

EXTRACTION_FIELDS = frozenset(
    (
        "configuration_digest",
        "extraction_id",
        "extractor_id",
        "extractor_version",
    )
)

FRAGMENT_FIELDS = frozenset(
    (
        "byte_end",
        "byte_start",
        "content_digest",
        "fragment_id",
        "sequence_number",
    )
)

DIGEST_FIELDS = frozenset(
    (
        "algorithm",
        "value",
    )
)


def validate_knowledge_ingestion_registry_payload(
    *,
    payload: str,
) -> bool:
    """Validate registry JSON structure without asserting integrity."""

    if not isinstance(
        payload,
        str,
    ):
        raise TypeError(
            "payload must be a string"
        )

    if not payload.strip():
        raise ValueError(
            "payload must not be empty"
        )

    try:
        document = json.loads(
            payload,
        )
    except (
        json.JSONDecodeError,
        UnicodeDecodeError,
    ) as error:
        raise ValueError(
            "payload must contain valid JSON"
        ) from error

    if not isinstance(
        document,
        dict,
    ):
        raise ValueError(
            "registry payload must be a JSON object"
        )

    _validate_fields(
        document=document,
        expected=ROOT_FIELDS,
        subject="registry",
    )

    schema_version = document[
        "schema_version"
    ]

    if (
        isinstance(
            schema_version,
            bool,
        )
        or not isinstance(
            schema_version,
            int,
        )
        or schema_version
        != KNOWLEDGE_INGESTION_REGISTRY_SCHEMA_VERSION
    ):
        raise ValueError(
            "schema_version must equal supported version 1"
        )

    records = document[
        "records"
    ]

    if not isinstance(
        records,
        list,
    ):
        raise ValueError(
            "records must be a JSON array"
        )

    ingestion_ids = set()
    artifact_keys = set()

    for record in records:
        _validate_record(
            record=record,
            ingestion_ids=ingestion_ids,
            artifact_keys=artifact_keys,
        )

    return True


def _validate_record(
    *,
    record: object,
    ingestion_ids: set,
    artifact_keys: set,
) -> None:
    if not isinstance(
        record,
        dict,
    ):
        raise ValueError(
            "registry record must be a JSON object"
        )

    _validate_fields(
        document=record,
        expected=RECORD_FIELDS,
        subject="registry record",
    )

    ingestion_id = _validate_identity(
        value=record["ingestion_id"],
        field="ingestion_id",
    )

    if ingestion_id in ingestion_ids:
        raise ValueError(
            "ingestion_id must be unique"
        )

    ingestion_ids.add(
        ingestion_id,
    )

    artifact = record[
        "artifact"
    ]

    if not isinstance(
        artifact,
        dict,
    ):
        raise ValueError(
            "artifact must be a JSON object"
        )

    _validate_fields(
        document=artifact,
        expected=ARTIFACT_FIELDS,
        subject="artifact",
    )

    artifact_id = _validate_identity(
        value=artifact["artifact_id"],
        field="artifact_id",
    )

    artifact_version = _validate_identity(
        value=artifact["artifact_version"],
        field="artifact_version",
    )

    artifact_key = (
        artifact_id,
        artifact_version,
    )

    if artifact_key in artifact_keys:
        raise ValueError(
            "artifact identity and version must be unique"
        )

    artifact_keys.add(
        artifact_key,
    )

    _validate_source(
        source=artifact["source"],
    )

    _validate_extraction(
        extraction=artifact["extraction"],
    )

    _validate_digest(
        digest=artifact["content_digest"],
        field="artifact content_digest",
    )

    fragments = record[
        "fragments"
    ]

    if not isinstance(
        fragments,
        list,
    ):
        raise ValueError(
            "fragments must be a JSON array"
        )

    fragment_ids = set()
    sequence_numbers = set()

    for fragment in fragments:
        _validate_fragment(
            fragment=fragment,
            fragment_ids=fragment_ids,
            sequence_numbers=sequence_numbers,
        )


def _validate_source(
    *,
    source: object,
) -> None:
    if not isinstance(
        source,
        dict,
    ):
        raise ValueError(
            "source must be a JSON object"
        )

    _validate_fields(
        document=source,
        expected=SOURCE_FIELDS,
        subject="source",
    )

    _validate_identity(
        value=source["source_id"],
        field="source_id",
    )

    _validate_identity(
        value=source["source_version"],
        field="source_version",
    )

    _validate_digest(
        digest=source["content_digest"],
        field="source content_digest",
    )


def _validate_extraction(
    *,
    extraction: object,
) -> None:
    if not isinstance(
        extraction,
        dict,
    ):
        raise ValueError(
            "extraction must be a JSON object"
        )

    _validate_fields(
        document=extraction,
        expected=EXTRACTION_FIELDS,
        subject="extraction",
    )

    for field in (
        "extraction_id",
        "extractor_id",
        "extractor_version",
    ):
        _validate_identity(
            value=extraction[field],
            field=field,
        )

    _validate_digest(
        digest=extraction["configuration_digest"],
        field="configuration_digest",
    )


def _validate_fragment(
    *,
    fragment: object,
    fragment_ids: set,
    sequence_numbers: set,
) -> None:
    if not isinstance(
        fragment,
        dict,
    ):
        raise ValueError(
            "fragment must be a JSON object"
        )

    _validate_fields(
        document=fragment,
        expected=FRAGMENT_FIELDS,
        subject="fragment",
    )

    fragment_id = _validate_identity(
        value=fragment["fragment_id"],
        field="fragment_id",
    )

    if fragment_id in fragment_ids:
        raise ValueError(
            "fragment_id must be unique within artifact"
        )

    fragment_ids.add(
        fragment_id,
    )

    sequence_number = _validate_non_negative_integer(
        value=fragment["sequence_number"],
        field="sequence_number",
    )

    if sequence_number in sequence_numbers:
        raise ValueError(
            "sequence_number must be unique within artifact"
        )

    sequence_numbers.add(
        sequence_number,
    )

    byte_start = _validate_non_negative_integer(
        value=fragment["byte_start"],
        field="byte_start",
    )

    byte_end = _validate_positive_integer(
        value=fragment["byte_end"],
        field="byte_end",
    )

    if byte_end <= byte_start:
        raise ValueError(
            "byte_end must be greater than byte_start"
        )

    _validate_digest(
        digest=fragment["content_digest"],
        field="fragment content_digest",
    )


def _validate_digest(
    *,
    digest: object,
    field: str,
) -> None:
    if not isinstance(
        digest,
        dict,
    ):
        raise ValueError(
            f"{field} must be a JSON object"
        )

    _validate_fields(
        document=digest,
        expected=DIGEST_FIELDS,
        subject=field,
    )

    if digest["algorithm"] != "SHA-256":
        raise ValueError(
            f"{field} algorithm must be SHA-256"
        )

    value = digest[
        "value"
    ]

    if (
        not isinstance(
            value,
            str,
        )
        or re.fullmatch(
            r"[0-9a-f]{64}",
            value,
        )
        is None
    ):
        raise ValueError(
            f"{field} value must contain "
            "64 lowercase hexadecimal characters"
        )


def _validate_fields(
    *,
    document: dict,
    expected: frozenset,
    subject: str,
) -> None:
    present = frozenset(
        document
    )

    missing = (
        expected
        - present
    )

    if missing:
        raise ValueError(
            f"missing required {subject} fields: "
            + ", ".join(
                sorted(
                    missing
                )
            )
        )

    unexpected = (
        present
        - expected
    )

    if unexpected:
        raise ValueError(
            f"unexpected {subject} fields: "
            + ", ".join(
                sorted(
                    unexpected
                )
            )
        )


def _validate_identity(
    *,
    value: object,
    field: str,
) -> str:
    if (
        not isinstance(
            value,
            str,
        )
        or not value.strip()
    ):
        raise ValueError(
            f"{field} must not be empty"
        )

    return value


def _validate_positive_integer(
    *,
    value: object,
    field: str,
) -> int:
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value < 1
    ):
        raise ValueError(
            f"{field} must be a positive integer"
        )

    return value


def _validate_non_negative_integer(
    *,
    value: object,
    field: str,
) -> int:
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value < 0
    ):
        raise ValueError(
            f"{field} must be a non-negative integer"
        )

    return value
