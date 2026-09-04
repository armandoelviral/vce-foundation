import ast
from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope as exchange_module
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL,
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION,
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
    build_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from test_knowledge_governed_retrieval_evidence_artifact import (
    create_artifact,
)


def create_envelope():
    return build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=create_artifact(),
    )


def test_exchange_protocol_metadata_is_exact() -> None:
    assert KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL == (
        "sp001.knowledge-governed-retrieval-evidence"
    )
    assert KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION == 1
    assert KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE == (
        "application/vnd.sp001.knowledge-governed-retrieval-evidence+json"
    )
    assert KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING == "UTF-8"


def test_exchange_envelope_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(
        KnowledgeGovernedRetrievalEvidenceExchangeEnvelope
    )) == (
        "protocol",
        "protocol_version",
        "media_type",
        "encoding",
        "artifact",
    )


def test_exchange_envelope_is_immutable() -> None:
    envelope = create_envelope()
    with pytest.raises(FrozenInstanceError):
        envelope.protocol = "changed"


def test_exchange_envelope_uses_slots() -> None:
    assert not hasattr(create_envelope(), "__dict__")


def test_builder_sets_exact_protocol_metadata() -> None:
    envelope = create_envelope()
    assert envelope.protocol == KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL
    assert envelope.protocol_version == (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_PROTOCOL_VERSION
    )
    assert envelope.media_type == (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_MEDIA_TYPE
    )
    assert envelope.encoding == (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_EXCHANGE_ENCODING
    )


def test_builder_preserves_exact_artifact_reference() -> None:
    artifact = create_artifact()
    envelope = build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=artifact,
    )
    assert envelope.artifact is artifact


def test_builder_is_deterministic_for_same_artifact() -> None:
    artifact = create_artifact()
    first = build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=artifact,
    )
    second = build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=artifact,
    )
    assert first == second


@pytest.mark.parametrize("value", (None, 1, b"protocol"))
def test_protocol_requires_string(value) -> None:
    envelope = create_envelope()
    with pytest.raises(TypeError, match="protocol must be a string"):
        replace(envelope, protocol=value)


def test_protocol_requires_supported_value() -> None:
    with pytest.raises(ValueError, match="protocol must equal supported"):
        replace(create_envelope(), protocol="unsupported")


@pytest.mark.parametrize("value", (None, True, "1", 1.0))
def test_protocol_version_requires_strict_integer(value) -> None:
    with pytest.raises(TypeError, match="protocol_version must be an integer"):
        replace(create_envelope(), protocol_version=value)


@pytest.mark.parametrize("value", (0, 2, -1))
def test_protocol_version_requires_supported_value(value: int) -> None:
    with pytest.raises(ValueError, match="protocol_version must equal supported version 1"):
        replace(create_envelope(), protocol_version=value)


@pytest.mark.parametrize("value", (None, 1, b"application/json"))
def test_media_type_requires_string(value) -> None:
    with pytest.raises(TypeError, match="media_type must be a string"):
        replace(create_envelope(), media_type=value)


def test_media_type_requires_supported_value() -> None:
    with pytest.raises(ValueError, match="media_type must equal supported exchange media type"):
        replace(create_envelope(), media_type="application/json")


@pytest.mark.parametrize("value", (None, 1, b"UTF-8"))
def test_encoding_requires_string(value) -> None:
    with pytest.raises(TypeError, match="encoding must be a string"):
        replace(create_envelope(), encoding=value)


@pytest.mark.parametrize("value", ("utf-8", "UTF-16"))
def test_encoding_requires_exact_supported_value(value: str) -> None:
    with pytest.raises(ValueError, match="encoding must be UTF-8"):
        replace(create_envelope(), encoding=value)


@pytest.mark.parametrize("value", (None, {}, "artifact"))
def test_artifact_requires_exact_type(value) -> None:
    with pytest.raises(
        TypeError,
        match="artifact must be a KnowledgeGovernedRetrievalEvidenceArtifact",
    ):
        replace(create_envelope(), artifact=value)


def test_builder_rejects_untyped_artifact() -> None:
    with pytest.raises(
        TypeError,
        match="artifact must be a KnowledgeGovernedRetrievalEvidenceArtifact",
    ):
        build_knowledge_governed_retrieval_evidence_exchange_envelope(
            artifact=None,
        )


def test_contract_does_not_verify_typed_artifact() -> None:
    artifact = create_artifact()
    unverified = replace(
        artifact,
        payload=artifact.payload + " ",
    )
    envelope = build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=unverified,
    )
    assert envelope.artifact is unverified


def test_contract_introduces_no_serialization_verification_or_io() -> None:
    source = Path(exchange_module.__file__).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module is not None
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }
    assert not any(
        boundary in module
        for module in imported_modules
        for boundary in (
            "serialization",
            "verification",
            "storage",
            "atomic_write",
            "artifact_read",
            "recovery",
        )
    )
    assert not {
        "dumps",
        "loads",
        "encode",
        "decode",
        "sha256",
        "compare_digest",
        "open",
        "read",
        "write",
    } & called_names


def test_contract_has_no_delivery_identity_or_authenticity_metadata() -> None:
    names = {
        field.name.casefold()
        for field in fields(KnowledgeGovernedRetrievalEvidenceExchangeEnvelope)
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
