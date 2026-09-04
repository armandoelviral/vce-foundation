import ast
import copy
import json

from dataclasses import replace
from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization as serialization_module
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization import (
    serialize_knowledge_governed_retrieval_evidence_artifact,
)
from test_knowledge_governed_retrieval_evidence_artifact_verification import (
    create_artifact,
    replace_payload_with_matching_digest,
)


def serialize(artifact=None) -> str:
    return serialize_knowledge_governed_retrieval_evidence_artifact(
        artifact=(
            artifact
            if artifact is not None
            else create_artifact()
        ),
    )


def test_storage_serializer_returns_text() -> None:
    assert isinstance(serialize(), str)


def test_storage_envelope_has_exact_root_fields() -> None:
    assert frozenset(json.loads(serialize())) == frozenset(
        (
            "digest",
            "media_type",
            "payload",
            "schema_version",
        )
    )


def test_storage_envelope_preserves_exact_payload() -> None:
    artifact = create_artifact()
    assert json.loads(serialize(artifact))["payload"] == artifact.payload


def test_storage_envelope_preserves_complete_digest() -> None:
    artifact = create_artifact()
    assert json.loads(serialize(artifact))["digest"] == {
        "algorithm": artifact.digest.algorithm,
        "encoding": artifact.digest.encoding,
        "value": artifact.digest.value,
    }


def test_storage_envelope_preserves_media_type_and_schema_version() -> None:
    artifact = create_artifact()
    document = json.loads(serialize(artifact))
    assert document["media_type"] == artifact.media_type
    assert document["schema_version"] == artifact.schema_version


def test_storage_serialization_is_deterministic() -> None:
    artifact = create_artifact()
    assert serialize(artifact) == serialize(artifact)


def test_storage_serialization_uses_compact_sorted_json() -> None:
    stored = serialize()
    document = json.loads(stored)
    assert stored == json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    assert "\n" not in stored
    assert ": " not in stored


def test_storage_serialization_preserves_unicode() -> None:
    artifact = create_artifact()
    document = json.loads(artifact.payload)
    document["result"]["query"]["query_id"] = "CONSULTA-Á"
    document["result"]["lexical_ordering"]["query"]["query_id"] = (
        "CONSULTA-Á"
    )
    document["result"]["lexical_ordering"]["entries"][0][
        "evidence"
    ]["match"]["query"]["query_id"] = "CONSULTA-Á"
    payload = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    artifact = replace_payload_with_matching_digest(
        artifact,
        payload,
    )
    stored = serialize(artifact)
    assert "Á" in stored
    assert "\\u00c1" not in stored
    assert json.loads(stored)["payload"] == payload


@pytest.mark.parametrize("invalid_artifact", (None, {}, (), "artifact"))
def test_storage_serialization_rejects_untyped_artifact(
    invalid_artifact: object,
) -> None:
    with pytest.raises(TypeError, match="artifact must be"):
        serialize_knowledge_governed_retrieval_evidence_artifact(
            artifact=invalid_artifact,
        )


def test_storage_serialization_blocks_digest_mismatch() -> None:
    artifact = create_artifact()
    artifact = replace(
        artifact,
        payload=artifact.payload + " ",
    )
    with pytest.raises(ValueError, match="verification failed"):
        serialize(artifact)


def test_storage_serialization_blocks_invalid_structure() -> None:
    artifact = replace_payload_with_matching_digest(
        create_artifact(),
        "{}",
    )
    with pytest.raises(ValueError, match="missing required"):
        serialize(artifact)


def test_verification_false_blocks_envelope_projection(monkeypatch) -> None:
    artifact = create_artifact()
    monkeypatch.setattr(
        serialization_module,
        "verify_received_knowledge_governed_retrieval_evidence_artifact",
        lambda *, artifact: False,
    )
    with pytest.raises(ValueError, match="verification failed"):
        serialize(artifact)


def test_storage_serialization_does_not_mutate_artifact() -> None:
    artifact = create_artifact()
    before = copy.deepcopy(artifact)
    serialize(artifact)
    assert artifact == before


def test_storage_serializer_has_no_filesystem_transport_or_authenticity_capability() -> None:
    source = Path(
        serialization_module.__file__
    ).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    called_attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
    }
    assert not {
        "mkdir",
        "open",
        "read_text",
        "read_bytes",
        "write_text",
        "write_bytes",
        "replace",
        "rename",
        "unlink",
    } & called_attributes
    assert "http" not in source.casefold()
    assert "authentic" not in source.casefold()
