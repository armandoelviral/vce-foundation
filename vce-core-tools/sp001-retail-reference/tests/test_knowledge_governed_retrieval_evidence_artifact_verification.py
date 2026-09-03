import ast
import hashlib
import json

from dataclasses import replace
from pathlib import Path

import pytest

import sp001.services.knowledge_governed_retrieval_evidence_artifact_verification as verification_module
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    build_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact_verification import (
    verify_received_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def create_artifact():
    return build_knowledge_governed_retrieval_evidence_artifact(
        evidence=create_mixed_evidence(),
    )


def replace_payload_with_matching_digest(artifact, payload: str):
    digest = replace(
        artifact.digest,
        value=hashlib.sha256(
            payload.encode("UTF-8", errors="strict")
        ).hexdigest(),
    )
    return replace(
        artifact,
        payload=payload,
        digest=digest,
    )


def test_valid_received_artifact_passes() -> None:
    assert verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=create_artifact(),
    )


def test_digest_is_calculated_over_exact_noncanonical_received_bytes() -> None:
    artifact = create_artifact()
    payload = json.dumps(
        json.loads(artifact.payload),
        indent=2,
        ensure_ascii=False,
    )
    received = replace_payload_with_matching_digest(
        artifact,
        payload,
    )
    assert payload != artifact.payload
    assert verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=received,
    )


def test_changed_payload_with_original_digest_returns_false() -> None:
    artifact = create_artifact()
    changed = replace(
        artifact,
        payload=artifact.payload + " ",
    )
    assert not verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=changed,
    )


def test_well_formed_incorrect_digest_returns_false() -> None:
    artifact = create_artifact()
    changed = replace(
        artifact,
        digest=replace(
            artifact.digest,
            value="0" * 64,
        ),
    )
    assert not verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=changed,
    )


def test_digest_mismatch_never_invokes_structural_validation(
    monkeypatch,
) -> None:
    artifact = create_artifact()
    changed = replace(
        artifact,
        payload=artifact.payload + " ",
    )

    def fail_if_called(*, payload: str) -> bool:
        raise AssertionError(
            f"structural validation received {payload!r}"
        )

    monkeypatch.setattr(
        verification_module,
        "validate_knowledge_governed_retrieval_evidence_payload",
        fail_if_called,
    )
    assert not verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=changed,
    )


def test_matching_digest_invokes_structural_validation(
    monkeypatch,
) -> None:
    artifact = create_artifact()
    observed = []

    def observe(*, payload: str) -> bool:
        observed.append(payload)
        return True

    monkeypatch.setattr(
        verification_module,
        "validate_knowledge_governed_retrieval_evidence_payload",
        observe,
    )
    assert verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=artifact,
    )
    assert observed == [artifact.payload]


@pytest.mark.parametrize("invalid_artifact", (None, {}, (), "artifact"))
def test_non_artifact_input_is_rejected(invalid_artifact: object) -> None:
    with pytest.raises(TypeError, match="artifact must be"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=invalid_artifact,
        )


def test_invalid_digest_object_type_is_rejected() -> None:
    artifact = create_artifact()
    with pytest.raises(TypeError, match="artifact digest must be"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=replace(artifact, digest=None),
        )


@pytest.mark.parametrize("invalid_payload", (None, b"{}", {}, ()))
def test_non_string_payload_is_rejected(invalid_payload: object) -> None:
    artifact = replace(
        create_artifact(),
        payload=invalid_payload,
    )
    with pytest.raises(TypeError, match="payload must be a string"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


def test_payload_that_cannot_be_encoded_as_utf8_is_rejected() -> None:
    artifact = replace(
        create_artifact(),
        payload="\ud800",
    )
    with pytest.raises(ValueError, match="valid UTF-8"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize("media_type", (None, "text/plain", "APPLICATION/JSON"))
def test_invalid_media_type_is_rejected(media_type: object) -> None:
    artifact = replace(
        create_artifact(),
        media_type=media_type,
    )
    with pytest.raises(ValueError, match="media_type"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize("schema_version", (None, True, False, 0, 2, "1"))
def test_invalid_artifact_schema_version_is_rejected(
    schema_version: object,
) -> None:
    artifact = replace(
        create_artifact(),
        schema_version=schema_version,
    )
    with pytest.raises(ValueError, match="schema_version"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize("algorithm", (None, "sha256", "SHA-512"))
def test_invalid_digest_algorithm_is_rejected(algorithm: object) -> None:
    artifact = create_artifact()
    artifact = replace(
        artifact,
        digest=replace(
            artifact.digest,
            algorithm=algorithm,
        ),
    )
    with pytest.raises(ValueError, match="algorithm"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize("encoding", (None, "utf-8", "ASCII"))
def test_invalid_digest_encoding_is_rejected(encoding: object) -> None:
    artifact = create_artifact()
    artifact = replace(
        artifact,
        digest=replace(
            artifact.digest,
            encoding=encoding,
        ),
    )
    with pytest.raises(ValueError, match="encoding"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


@pytest.mark.parametrize(
    "value",
    (None, True, "", "0" * 63, "0" * 65, "G" * 64, "A" * 64),
)
def test_invalid_digest_value_is_rejected(value: object) -> None:
    artifact = create_artifact()
    artifact = replace(
        artifact,
        digest=replace(
            artifact.digest,
            value=value,
        ),
    )
    with pytest.raises(ValueError, match="64 lowercase hexadecimal"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


def test_structurally_invalid_payload_is_rejected_after_digest_match() -> None:
    artifact = replace_payload_with_matching_digest(
        create_artifact(),
        "{}",
    )
    with pytest.raises(ValueError, match="missing required"):
        verify_received_knowledge_governed_retrieval_evidence_artifact(
            artifact=artifact,
        )


def test_unicode_payload_identity_uses_exact_utf8_bytes() -> None:
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
    assert "Á" in payload
    assert verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=artifact,
    )


def test_compare_digest_receives_computed_and_declared_values(
    monkeypatch,
) -> None:
    artifact = create_artifact()
    observed = []

    def compare(computed: str, declared: str) -> bool:
        observed.append((computed, declared))
        return False

    monkeypatch.setattr(
        verification_module.hmac,
        "compare_digest",
        compare,
    )
    assert not verify_received_knowledge_governed_retrieval_evidence_artifact(
        artifact=artifact,
    )
    assert observed == [
        (
            hashlib.sha256(
                artifact.payload.encode("UTF-8")
            ).hexdigest(),
            artifact.digest.value,
        )
    ]


def test_verifier_does_not_reconstruct_domain_evidence_or_claim_authenticity() -> None:
    source = Path(
        verification_module.__file__
    ).read_text(encoding="UTF-8")
    tree = ast.parse(source)
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
    }
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    assert "KnowledgeGovernedRetrievalEvidence" not in imported_names
    assert "KnowledgeGovernedRetrievalEvidence" not in called_names
    assert "deserialize" not in source
    assert "authentic" not in source.casefold()
    assert not {
        "digest_knowledge_governed_retrieval_evidence",
        "build_knowledge_governed_retrieval_evidence_artifact",
    } & called_names
