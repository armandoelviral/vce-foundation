import ast
from dataclasses import fields
import hashlib
import hmac
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_exchange_acceptance as acceptance_module
from sp001.services.knowledge_governed_retrieval_evidence_exchange_acceptance import (
    InvalidRetrievalEvidenceExchangeArtifactError,
    KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError,
    NoncanonicalRetrievalEvidenceExchangeEnvelopeError,
    accept_received_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_parsing import (
    InvalidRetrievalEvidenceExchangeStructureError,
    MalformedRetrievalEvidenceExchangeEnvelopeError,
    UnsupportedRetrievalEvidenceExchangeMetadataError,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_serialization import (
    serialize_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from test_knowledge_governed_retrieval_evidence_exchange_envelope import (
    create_envelope,
)
from test_knowledge_governed_retrieval_evidence_exchange_serialization import (
    create_unicode_envelope,
)


def serialize_valid_envelope() -> str:
    return serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
        envelope=create_envelope(),
    )


def create_document() -> dict:
    return json.loads(serialize_valid_envelope())


def serialize_document(document: object) -> str:
    return json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def test_acceptance_error_hierarchy_is_exact() -> None:
    assert issubclass(
        InvalidRetrievalEvidenceExchangeArtifactError,
        KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError,
    )
    assert issubclass(
        NoncanonicalRetrievalEvidenceExchangeEnvelopeError,
        KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError,
    )
    assert issubclass(
        KnowledgeGovernedRetrievalEvidenceExchangeAcceptanceError,
        ValueError,
    )


@pytest.mark.parametrize("value", (None, b"{}", {}, 1))
def test_acceptance_requires_received_string(value) -> None:
    with pytest.raises(
        TypeError,
        match="received_envelope must be a string",
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=value,
        )


def test_acceptance_returns_typed_exchange_envelope() -> None:
    accepted = (
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_valid_envelope(),
        )
    )
    assert isinstance(
        accepted,
        KnowledgeGovernedRetrievalEvidenceExchangeEnvelope,
    )


def test_acceptance_preserves_received_values() -> None:
    received = serialize_valid_envelope()
    document = json.loads(received)
    accepted = (
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )
    )
    assert accepted.protocol == document["protocol"]
    assert accepted.protocol_version == document["protocol_version"]
    assert accepted.media_type == document["media_type"]
    assert accepted.encoding == document["encoding"]
    assert accepted.artifact.payload == document["artifact"]["payload"]
    assert accepted.artifact.digest.value == (
        document["artifact"]["digest"]["value"]
    )


def test_acceptance_preserves_unicode() -> None:
    envelope = create_unicode_envelope()
    received = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    accepted = (
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )
    )
    assert accepted.artifact.payload == envelope.artifact.payload
    assert "niñez café 東京" in accepted.artifact.payload


@pytest.mark.parametrize("value", ("", "{", "not-json"))
def test_malformed_exchange_error_propagates(value: str) -> None:
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=value,
        )


def test_structural_exchange_error_propagates() -> None:
    document = create_document()
    del document["artifact"]
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeStructureError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_document(document),
        )


def test_unsupported_metadata_error_propagates() -> None:
    document = create_document()
    document["protocol_version"] = 2
    with pytest.raises(
        UnsupportedRetrievalEvidenceExchangeMetadataError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_document(document),
        )


def test_digest_mismatch_is_classified_as_invalid_artifact() -> None:
    document = create_document()
    document["artifact"]["payload"] += " "
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeArtifactError,
        match="exchange envelope artifact must pass verification",
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_document(document),
        )


def test_structurally_invalid_payload_with_matching_digest_is_invalid_artifact() -> None:
    document = create_document()
    payload = "{}"
    document["artifact"]["payload"] = payload
    document["artifact"]["digest"]["value"] = hashlib.sha256(
        payload.encode("UTF-8")
    ).hexdigest()
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeArtifactError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_document(document),
        )


@pytest.mark.parametrize(
    "received",
    (
        lambda: json.dumps(create_document(), indent=2),
        lambda: json.dumps(create_document(), separators=(", ", ": ")),
        lambda: serialize_valid_envelope() + "\n",
    ),
)
def test_equivalent_noncanonical_json_is_rejected(received) -> None:
    with pytest.raises(
        NoncanonicalRetrievalEvidenceExchangeEnvelopeError,
        match="must be canonical UTF-8 JSON",
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received(),
        )


def test_ascii_escaped_unicode_exchange_is_rejected() -> None:
    envelope = create_unicode_envelope()
    canonical = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    escaped = json.dumps(
        json.loads(canonical),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    assert escaped != canonical
    with pytest.raises(
        NoncanonicalRetrievalEvidenceExchangeEnvelopeError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=escaped,
        )


def test_compare_digest_receives_exact_utf8_bytes(monkeypatch) -> None:
    received = serialize_valid_envelope()
    comparisons = []
    original = hmac.compare_digest

    def compare(left, right):
        comparisons.append((left, right))
        return original(left, right)

    monkeypatch.setattr(
        acceptance_module,
        "hmac",
        SimpleNamespace(compare_digest=compare),
    )
    accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
        received_envelope=received,
    )
    assert len(comparisons) == 1
    assert comparisons[0][0] == received.encode("UTF-8")
    assert isinstance(comparisons[0][1], bytes)
    assert comparisons[0][0] == comparisons[0][1]


def test_parsing_failure_blocks_canonicalization_and_comparison(
    monkeypatch,
) -> None:
    events = []

    def reject_parser(*, received_envelope):
        events.append("parse")
        raise MalformedRetrievalEvidenceExchangeEnvelopeError("malformed")

    def forbidden_canonicalization(*, envelope):
        events.append("canonicalize")
        raise AssertionError("canonicalization must not run")

    def forbidden_comparison(left, right):
        events.append("compare")
        raise AssertionError("comparison must not run")

    monkeypatch.setattr(
        acceptance_module,
        "parse_received_knowledge_governed_retrieval_evidence_exchange_envelope",
        reject_parser,
    )
    monkeypatch.setattr(
        acceptance_module,
        "canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes",
        forbidden_canonicalization,
    )
    monkeypatch.setattr(
        acceptance_module,
        "hmac",
        SimpleNamespace(compare_digest=forbidden_comparison),
    )
    with pytest.raises(
        MalformedRetrievalEvidenceExchangeEnvelopeError,
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope="malformed",
        )
    assert events == ["parse"]


def test_artifact_failure_blocks_comparison(monkeypatch) -> None:
    events = []

    def reject_canonicalization(*, envelope):
        events.append("canonicalize")
        raise ValueError("invalid artifact")

    def forbidden_comparison(left, right):
        events.append("compare")
        raise AssertionError("comparison must not run")

    monkeypatch.setattr(
        acceptance_module,
        "canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes",
        reject_canonicalization,
    )
    monkeypatch.setattr(
        acceptance_module,
        "hmac",
        SimpleNamespace(compare_digest=forbidden_comparison),
    )
    with pytest.raises(
        InvalidRetrievalEvidenceExchangeArtifactError,
        match="invalid artifact",
    ):
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=serialize_valid_envelope(),
        )
    assert events == ["canonicalize"]


def test_canonicalization_is_invoked_exactly_once(monkeypatch) -> None:
    received = serialize_valid_envelope()
    original = (
        acceptance_module.canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes
    )
    calls = []

    def canonicalize(*, envelope):
        calls.append(envelope)
        return original(envelope=envelope)

    monkeypatch.setattr(
        acceptance_module,
        "canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes",
        canonicalize,
    )
    accepted = (
        accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
            received_envelope=received,
        )
    )
    assert calls == [accepted]


def test_acceptance_does_not_mutate_received_text() -> None:
    received = serialize_valid_envelope()
    before = received
    accept_received_knowledge_governed_retrieval_evidence_exchange_envelope(
        received_envelope=received,
    )
    assert received == before


def test_service_uses_composed_boundaries_without_direct_artifact_verifier() -> None:
    source = Path(acceptance_module.__file__).read_text(
        encoding="UTF-8"
    )
    tree = ast.parse(source)
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert (
        "parse_received_knowledge_governed_retrieval_evidence_exchange_envelope"
        in imported_names
    )
    assert (
        "canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes"
        in imported_names
    )
    assert (
        "verify_received_knowledge_governed_retrieval_evidence_artifact"
        not in imported_names
    )


def test_service_introduces_no_io_transport_or_authenticity_claim() -> None:
    source = Path(acceptance_module.__file__).read_text(
        encoding="UTF-8"
    )
    tree = ast.parse(source)
    attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
    }
    assert not attributes & {
        "loads",
        "dumps",
        "open",
        "read",
        "write",
        "send",
        "recv",
        "connect",
    }
    assert "authentic" not in source.casefold()


def test_acceptance_adds_no_delivery_or_identity_fields() -> None:
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
