import ast
from dataclasses import replace
import json
from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_exchange_serialization as serialization_module
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    build_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_envelope import (
    build_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from sp001.services.knowledge_governed_retrieval_evidence_exchange_serialization import (
    canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes,
    serialize_knowledge_governed_retrieval_evidence_exchange_envelope,
)
from test_knowledge_governed_retrieval_evidence_exchange_envelope import (
    create_envelope,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def create_unicode_envelope():
    artifact = build_knowledge_governed_retrieval_evidence_artifact(
        evidence=create_mixed_evidence(
            raw_text="niñez café 東京",
        ),
    )
    return build_knowledge_governed_retrieval_evidence_exchange_envelope(
        artifact=artifact,
    )


def test_serialization_returns_string() -> None:
    assert isinstance(
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=create_envelope(),
        ),
        str,
    )


def test_serialized_root_fields_are_exact() -> None:
    envelope = create_envelope()
    document = json.loads(
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    assert tuple(document) == (
        "artifact",
        "encoding",
        "media_type",
        "protocol",
        "protocol_version",
    )


def test_serialized_protocol_metadata_is_preserved() -> None:
    envelope = create_envelope()
    document = json.loads(
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    assert document["protocol"] == envelope.protocol
    assert document["protocol_version"] == envelope.protocol_version
    assert document["media_type"] == envelope.media_type
    assert document["encoding"] == envelope.encoding


def test_serialized_artifact_fields_are_exact() -> None:
    envelope = create_envelope()
    document = json.loads(
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    assert tuple(document["artifact"]) == (
        "digest",
        "media_type",
        "payload",
        "schema_version",
    )


def test_serialized_artifact_is_preserved_by_value() -> None:
    envelope = create_envelope()
    artifact = json.loads(
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )["artifact"]
    assert artifact == {
        "digest": {
            "algorithm": envelope.artifact.digest.algorithm,
            "encoding": envelope.artifact.digest.encoding,
            "value": envelope.artifact.digest.value,
        },
        "media_type": envelope.artifact.media_type,
        "payload": envelope.artifact.payload,
        "schema_version": envelope.artifact.schema_version,
    }


def test_serialization_is_compact_sorted_canonical_json() -> None:
    serialized = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=create_envelope(),
        )
    )
    document = json.loads(serialized)
    assert serialized == json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    assert "\n" not in serialized
    assert ": " not in serialized
    assert ", " not in serialized


def test_serialization_is_deterministic() -> None:
    envelope = create_envelope()
    first = serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
        envelope=envelope,
    )
    second = serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
        envelope=envelope,
    )
    assert first == second


def test_serialization_preserves_unicode_without_ascii_escaping() -> None:
    serialized = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=create_unicode_envelope(),
        )
    )
    assert "niñez café 東京" in serialized
    assert "\\u00f1" not in serialized
    assert "\\u6771" not in serialized


@pytest.mark.parametrize("value", (None, {}, "envelope", 1))
def test_serialization_rejects_untyped_envelope(value) -> None:
    with pytest.raises(
        TypeError,
        match=(
            "envelope must be a "
            "KnowledgeGovernedRetrievalEvidenceExchangeEnvelope"
        ),
    ):
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=value,
        )


def test_serialization_rejects_digest_mismatch() -> None:
    envelope = create_envelope()
    invalid_artifact = replace(
        envelope.artifact,
        payload=envelope.artifact.payload + " ",
    )
    invalid_envelope = replace(
        envelope,
        artifact=invalid_artifact,
    )
    with pytest.raises(
        ValueError,
        match="exchange envelope artifact must pass verification",
    ):
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=invalid_envelope,
        )


def test_false_verification_result_blocks_projection(monkeypatch) -> None:
    envelope = create_envelope()
    calls = []

    def reject(*, artifact):
        calls.append(artifact)
        return False

    def forbidden_dumps(*args, **kwargs):
        raise AssertionError("projection reached JSON serialization")

    monkeypatch.setattr(
        serialization_module,
        "verify_received_knowledge_governed_retrieval_evidence_artifact",
        reject,
    )
    monkeypatch.setattr(
        serialization_module.json,
        "dumps",
        forbidden_dumps,
    )
    with pytest.raises(
        ValueError,
        match="exchange envelope artifact must pass verification",
    ):
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    assert calls == [envelope.artifact]


def test_canonical_bytes_return_bytes() -> None:
    assert isinstance(
        canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes(
            envelope=create_envelope(),
        ),
        bytes,
    )


def test_canonical_bytes_are_exact_utf8_serialization() -> None:
    envelope = create_unicode_envelope()
    serialized = (
        serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
            envelope=envelope,
        )
    )
    assert (
        canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes(
            envelope=envelope,
        )
        == serialized.encode("UTF-8")
    )


@pytest.mark.parametrize("value", (None, {}, "envelope", 1))
def test_canonical_bytes_reject_untyped_envelope(value) -> None:
    with pytest.raises(TypeError, match="envelope must be a"):
        canonical_knowledge_governed_retrieval_evidence_exchange_envelope_bytes(
            envelope=value,
        )


def test_serialization_does_not_mutate_envelope() -> None:
    envelope = create_envelope()
    before = (
        envelope.protocol,
        envelope.protocol_version,
        envelope.media_type,
        envelope.encoding,
        envelope.artifact,
    )
    serialize_knowledge_governed_retrieval_evidence_exchange_envelope(
        envelope=envelope,
    )
    assert (
        envelope.protocol,
        envelope.protocol_version,
        envelope.media_type,
        envelope.encoding,
        envelope.artifact,
    ) == before


def test_service_performs_no_parsing_or_io() -> None:
    source = Path(serialization_module.__file__).read_text(
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
        "decode",
        "open",
        "read",
        "write",
        "send",
        "recv",
        "connect",
    }


def test_service_introduces_no_exchange_digest_or_authenticity_claim() -> None:
    source = Path(serialization_module.__file__).read_text(
        encoding="UTF-8"
    ).casefold()
    assert "hashlib" not in source
    assert "sha256" not in source
    assert "compare_digest" not in source
    assert "authentic" not in source
