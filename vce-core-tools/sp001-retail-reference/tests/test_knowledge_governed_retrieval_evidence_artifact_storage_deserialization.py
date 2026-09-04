import ast
import json

from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_deserialization as deserialization_module
from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KnowledgeGovernedRetrievalEvidenceArtifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_deserialization import (
    InvalidRetrievalEvidenceStorageStructureError,
    KnowledgeGovernedRetrievalEvidenceStorageError,
    MalformedRetrievalEvidenceStorageError,
    NoncanonicalRetrievalEvidenceStorageError,
    RetrievalEvidenceStorageIntegrityMismatchError,
    deserialize_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_storage_serialization import (
    serialize_knowledge_governed_retrieval_evidence_artifact,
)
from test_knowledge_governed_retrieval_evidence_artifact_verification import (
    create_artifact,
    replace_payload_with_matching_digest,
)


def create_stored_artifact(artifact=None) -> str:
    return serialize_knowledge_governed_retrieval_evidence_artifact(
        artifact=(
            artifact
            if artifact is not None
            else create_artifact()
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
    recovered = deserialize_knowledge_governed_retrieval_evidence_artifact(
        stored_artifact=create_stored_artifact(artifact),
    )
    assert recovered == artifact
    assert recovered is not artifact


def test_storage_round_trip_preserves_unicode() -> None:
    artifact = create_artifact()
    document = json.loads(artifact.payload)
    document["result"]["query"]["query_id"] = "CONSULTA-Á"
    document["result"]["lexical_ordering"]["query"]["query_id"] = (
        "CONSULTA-Á"
    )
    document["result"]["lexical_ordering"]["entries"][0][
        "evidence"
    ]["match"]["query"]["query_id"] = "CONSULTA-Á"
    artifact = replace_payload_with_matching_digest(
        artifact,
        encode(document),
    )
    stored = create_stored_artifact(artifact)
    recovered = deserialize_knowledge_governed_retrieval_evidence_artifact(
        stored_artifact=stored,
    )
    assert "Á" in stored
    assert recovered == artifact


def test_deserialization_returns_artifact_not_domain_evidence() -> None:
    recovered = deserialize_knowledge_governed_retrieval_evidence_artifact(
        stored_artifact=create_stored_artifact(),
    )
    assert isinstance(
        recovered,
        KnowledgeGovernedRetrievalEvidenceArtifact,
    )
    assert not isinstance(
        recovered,
        KnowledgeGovernedRetrievalEvidence,
    )


@pytest.mark.parametrize("stored_artifact", (None, {}, (), b"{}", 1))
def test_deserialization_rejects_non_text_input(
    stored_artifact: object,
) -> None:
    with pytest.raises(TypeError, match="stored_artifact must be a string"):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=stored_artifact,
        )


@pytest.mark.parametrize("stored_artifact", ("", " ", "\n", "\t"))
def test_deserialization_rejects_empty_input(stored_artifact: str) -> None:
    with pytest.raises(MalformedRetrievalEvidenceStorageError):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=stored_artifact,
        )


def test_deserialization_rejects_malformed_json() -> None:
    with pytest.raises(
        MalformedRetrievalEvidenceStorageError,
        match="valid JSON",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact="{",
        )


@pytest.mark.parametrize("document", ([], None, "artifact", 1, True))
def test_deserialization_rejects_non_object_root(document: object) -> None:
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="JSON object",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


@pytest.mark.parametrize(
    "field",
    ("digest", "media_type", "payload", "schema_version"),
)
def test_deserialization_rejects_missing_envelope_field(field: str) -> None:
    document = json.loads(create_stored_artifact())
    del document[field]
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="missing required storage envelope fields",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_deserialization_rejects_unexpected_envelope_field() -> None:
    document = json.loads(create_stored_artifact())
    document["authority"] = "UNSUPPORTED"
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="unexpected storage envelope fields",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


@pytest.mark.parametrize("digest", (None, [], "digest", 1, True))
def test_deserialization_rejects_non_object_digest(digest: object) -> None:
    document = json.loads(create_stored_artifact())
    document["digest"] = digest
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="stored digest must be a JSON object",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


@pytest.mark.parametrize("field", ("algorithm", "encoding", "value"))
def test_deserialization_rejects_missing_digest_field(field: str) -> None:
    document = json.loads(create_stored_artifact())
    del document["digest"][field]
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="missing required stored digest fields",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_deserialization_rejects_unexpected_digest_field() -> None:
    document = json.loads(create_stored_artifact())
    document["digest"]["signature"] = "UNSUPPORTED"
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="unexpected stored digest fields",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


@pytest.mark.parametrize(
    ("path", "value", "detail"),
    (
        (("digest", "algorithm"), "SHA-512", "algorithm"),
        (("digest", "encoding"), "ASCII", "encoding"),
        (("digest", "value"), "x", "lowercase hexadecimal"),
        (("media_type",), "text/plain", "media_type"),
        (("schema_version",), True, "schema_version"),
        (("payload",), None, "payload must be a string"),
    ),
)
def test_deserialization_rejects_invalid_artifact_metadata(
    path: tuple[str, ...],
    value: object,
    detail: str,
) -> None:
    document = json.loads(create_stored_artifact())
    target = document
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match=detail,
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_deserialization_rejects_payload_digest_mismatch() -> None:
    document = json.loads(create_stored_artifact())
    document["payload"] += " "
    with pytest.raises(
        RetrievalEvidenceStorageIntegrityMismatchError,
        match="integrity verification failed",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_matching_digest_cannot_validate_invalid_payload_structure() -> None:
    artifact = replace_payload_with_matching_digest(
        create_artifact(),
        "{}",
    )
    document = {
        "digest": {
            "algorithm": artifact.digest.algorithm,
            "encoding": artifact.digest.encoding,
            "value": artifact.digest.value,
        },
        "media_type": artifact.media_type,
        "payload": artifact.payload,
        "schema_version": artifact.schema_version,
    }
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="missing required",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_deserialization_rejects_noncanonical_storage_json() -> None:
    document = json.loads(create_stored_artifact())
    noncanonical = json.dumps(
        document,
        indent=2,
        ensure_ascii=False,
    )
    with pytest.raises(
        NoncanonicalRetrievalEvidenceStorageError,
        match="canonical JSON",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=noncanonical,
        )


@pytest.mark.parametrize(
    "stored_artifact",
    (
        '{"digest":{},"digest":{},"media_type":"x","payload":"x","schema_version":1}',
        '{"digest":{"algorithm":"SHA-256","algorithm":"SHA-256","encoding":"UTF-8","value":"' + ("0" * 64) + '"},"media_type":"application/json","payload":"{}","schema_version":1}',
    ),
)
def test_deserialization_rejects_duplicate_envelope_or_digest_field(
    stored_artifact: str,
) -> None:
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="duplicate JSON field",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=stored_artifact,
        )


def test_deserialization_rejects_duplicate_payload_field() -> None:
    artifact = create_artifact()
    duplicated_payload = artifact.payload.replace(
        '{"counts":',
        '{"counts":{},"counts":',
        1,
    )
    artifact = replace_payload_with_matching_digest(
        artifact,
        duplicated_payload,
    )
    document = {
        "digest": {
            "algorithm": artifact.digest.algorithm,
            "encoding": artifact.digest.encoding,
            "value": artifact.digest.value,
        },
        "media_type": artifact.media_type,
        "payload": artifact.payload,
        "schema_version": artifact.schema_version,
    }
    with pytest.raises(
        InvalidRetrievalEvidenceStorageStructureError,
        match="duplicate JSON field: counts",
    ):
        deserialize_knowledge_governed_retrieval_evidence_artifact(
            stored_artifact=encode(document),
        )


def test_storage_error_hierarchy_is_typed_and_distinct() -> None:
    error_types = (
        MalformedRetrievalEvidenceStorageError,
        InvalidRetrievalEvidenceStorageStructureError,
        RetrievalEvidenceStorageIntegrityMismatchError,
        NoncanonicalRetrievalEvidenceStorageError,
    )
    assert all(
        issubclass(error_type, KnowledgeGovernedRetrievalEvidenceStorageError)
        for error_type in error_types
    )
    assert len(set(error_types)) == 4


def test_deserializer_has_no_filesystem_transport_or_authenticity_capability() -> None:
    source = Path(
        deserialization_module.__file__
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
    assert "KnowledgeGovernedRetrievalEvidence" not in {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
