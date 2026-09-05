import ast
from dataclasses import fields
import json
from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_exchange_parsing as parsing_module
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_parsing import (
    InvalidRetrievalEvidenceExchangeStructureError,
    KnowledgeGovernedRetrievalEvidenceExchangeParsingError,
    MalformedRetrievalEvidenceExchangeEnvelopeError,
    UnsupportedRetrievalEvidenceExchangeMetadataError,
    parse_received_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_serialization import (
    serialize_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from test_knowledge_governed_retrieval_evidence_exchange_envelope import (
    create_envelope,
)


def serialize_valid_envelope() -> str:
    return serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
        envelope=create_envelope(),
    )


def create_document() -> dict:
    return json.loads(serialize_valid_envelope())


def parse_document(document: object):
    return parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
        received_envelope=json.dumps(
            document,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ),
    )


def test_parsing_error_hierarchy_is_exact() -> None:
    assert issubclass(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
        KnowledgeGovernedRetrievalEvidenceExchangeParsingError,
    )
    assert issubclass(
        InvalidRetrievalEvidenceExchangeStructureError,
        KnowledgeGovernedRetrievalEvidenceExchangeParsingError,
    )
    assert issubclass(
        UnsupportedRetrievalEvidenceExchangeMetadataError,
        KnowledgeGovernedRetrievalEvidenceExchangeParsingError,
    )
    assert issubclass(
        KnowledgeGovernedRetrievalEvidenceExchangeParsingError,
        ValueError,
    )


@pytest.mark.parametrize("value", (None, b"{}", {}, 1))
def test_parser_requires_received_string(value) -> None:
    with pytest.raises(
        TypeError,
        match="received_envelope must be a string",
    ):
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=value,
        )


@pytest.mark.parametrize("value", ("", "{", "not-json", "[}"))
def test_malformed_json_is_distinct(value: str) -> None:
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
    ):
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=value,
        )


def test_duplicate_root_field_is_rejected() -> None:
    received = serialize_valid_envelope().replace(
        "{",
        '{"protocol":"duplicate",',
        1,
    )
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
        match="duplicate exchange field: protocol",
    ):
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )


def test_duplicate_artifact_field_is_rejected() -> None:
    received = serialize_valid_envelope().replace(
        '"payload":',
        '"payload":"duplicate","payload":',
        1,
    )
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
        match="duplicate exchange field: payload",
    ):
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )


def test_duplicate_digest_field_is_rejected() -> None:
    received = serialize_valid_envelope().replace(
        '"value":',
        '"value":"duplicate","value":',
        1,
    )
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
        match="duplicate exchange field: value",
    ):
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )


@pytest.mark.parametrize("value", (None, [], "root", 1))
def test_root_must_be_object(value) -> None:
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="exchange envelope must be an object",
    ):
        parse_document(value)


@pytest.mark.parametrize("field", ("protocol", "artifact"))
def test_root_rejects_missing_field(field: str) -> None:
    document = create_document()
    del document[field]
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="exchange envelope fields must be exactly",
    ):
        parse_document(document)


def test_root_rejects_additional_field() -> None:
    document = create_document()
    document["sender"] = "untrusted"
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="exchange envelope fields must be exactly",
    ):
        parse_document(document)


@pytest.mark.parametrize("value", (None, [], "artifact", 1))
def test_artifact_must_be_object(value) -> None:
    document = create_document()
    document["artifact"] = value
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact must be an object",
    ):
        parse_document(document)


def test_artifact_rejects_missing_or_additional_fields() -> None:
    missing = create_document()
    del missing["artifact"]["payload"]
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact fields must be exactly",
    ):
        parse_document(missing)
    additional = create_document()
    additional["artifact"]["signature"] = "unsupported"
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact fields must be exactly",
    ):
        parse_document(additional)


@pytest.mark.parametrize("value", (None, [], "digest", 1))
def test_digest_must_be_object(value) -> None:
    document = create_document()
    document["artifact"]["digest"] = value
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact.digest must be an object",
    ):
        parse_document(document)


def test_digest_rejects_missing_or_additional_fields() -> None:
    missing = create_document()
    del missing["artifact"]["digest"]["value"]
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact.digest fields must be exactly",
    ):
        parse_document(missing)
    additional = create_document()
    additional["artifact"]["digest"]["key_id"] = "unsupported"
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact.digest fields must be exactly",
    ):
        parse_document(additional)


@pytest.mark.parametrize(
    ("path", "value"),
    (
        (("protocol",), "unsupported"),
        (("protocol_version",), 2),
        (("media_type",), "application/json"),
        (("encoding",), "UTF-16"),
        (("artifact", "media_type"), "text/plain"),
        (("artifact", "schema_version"), 2),
        (("artifact", "digest", "algorithm"), "SHA-512"),
        (("artifact", "digest", "encoding"), "UTF-16"),
    ),
)
def test_unsupported_metadata_is_distinct(path, value) -> None:
    document = create_document()
    target = document
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    with pytest.raises(
        UnsupportedRetrievalEvidenceExchangeMetadataError,
        match="unsupported",
    ):
        parse_document(document)


@pytest.mark.parametrize(
    "path",
    (
        ("protocol",),
        ("media_type",),
        ("encoding",),
        ("artifact", "media_type"),
        ("artifact", "digest", "algorithm"),
        ("artifact", "digest", "encoding"),
    ),
)
def test_string_metadata_requires_string(path) -> None:
    document = create_document()
    target = document
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = 1
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="must be a string",
    ):
        parse_document(document)


@pytest.mark.parametrize(
    "path",
    (
        ("protocol_version",),
        ("artifact", "schema_version"),
    ),
)
@pytest.mark.parametrize("value", (True, "1", 1.0, None))
def test_integer_metadata_requires_strict_integer(path, value) -> None:
    document = create_document()
    target = document
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="must be an integer",
    ):
        parse_document(document)


@pytest.mark.parametrize("value", (None, {}, 1, []))
def test_payload_requires_string(value) -> None:
    document = create_document()
    document["artifact"]["payload"] = value
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="artifact.payload must be a string",
    ):
        parse_document(document)


@pytest.mark.parametrize(
    "value",
    (
        None,
        1,
        "0" * 63,
        "0" * 65,
        "A" * 64,
        "g" * 64,
    ),
)
def test_digest_value_requires_lowercase_sha256_shape(value) -> None:
    document = create_document()
    document["artifact"]["digest"]["value"] = value
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
        match="64 lowercase hexadecimal characters",
    ):
        parse_document(document)


def test_valid_exchange_materializes_exact_typed_graph() -> None:
    parsed = (
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_valid_envelope(),
        )
    )
    assert isinstance(
        parsed,
        KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
    )
    assert isinstance(
        parsed.artifact,
        KnowledgeGovernedRetrievalEvidenceArtifact,
    )
    assert isinstance(
        parsed.artifact.digest,
        KnowledgeGovernedRetrievalEvidenceDigest,
    )


def test_parsed_values_equal_serialized_values() -> None:
    document = create_document()
    parsed = parse_document(document)
    assert parsed.protocol == document["protocol"]
    assert parsed.protocol_version == document["protocol_version"]
    assert parsed.media_type == document["media_type"]
    assert parsed.encoding == document["encoding"]
    assert parsed.artifact.payload == document["artifact"]["payload"]
    assert parsed.artifact.digest.value == (
        document["artifact"]["digest"]["value"]
    )


def test_parser_does_not_verify_digest_correspondence() -> None:
    document = create_document()
    document["artifact"]["payload"] += " "
    parsed = parse_document(document)
    assert parsed.artifact.payload.endswith(" ")


def test_parser_accepts_noncanonical_exchange_json() -> None:
    received = json.dumps(
        create_document(),
        indent=2,
        ensure_ascii=False,
    )
    parsed = (
        parse_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )
    )
    assert isinstance(
        parsed,
        KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
    )


def test_parser_introduces_no_acceptance_or_io_capability() -> None:
    source = Path(parsing_module.__file__).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }
    assert not {
        "verify_received_knowledge_governed_retrieval_evidence_artifact",
        "serialize_knowledge_governed_retrieval_evidence_exchange_envelope",
        "canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes",
    } & imported_names
    assert not {
        "sha256",
        "compare_digest",
        "open",
        "read",
        "write",
        "send",
        "recv",
        "connect",
    } & called_names


def test_parser_adds_no_delivery_or_authenticity_fields() -> None:
    names = {
        field.name.casefold()
        for field in fields(
            KnowledgeGovernedRetrievalEvidenceExchangeEnvelope
        )
    }
    assert not names & {
        "timestamp",
        "sender",
        "recipient",
        "channel",
        "delivery_status",
        "signature",
        "authority",
        "authenticity",
    }
