import ast
import hashlib

from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
)
from sp001.services.knowledge_governed_retrieval_evidence_artifact import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE,
    KnowledgeGovernedRetrievalEvidenceArtifact,
    build_knowledge_governed_retrieval_evidence_artifact,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
    digest_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def create_artifact(
    *,
    raw_text: str = "governed planogram",
) -> KnowledgeGovernedRetrievalEvidenceArtifact:
    return build_knowledge_governed_retrieval_evidence_artifact(
        evidence=create_mixed_evidence(
            raw_text=raw_text,
        ),
    )


def test_artifact_builder_requires_validated_evidence() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidence",
    ):
        build_knowledge_governed_retrieval_evidence_artifact(
            evidence="evidence",  # type: ignore[arg-type]
        )


def test_builder_returns_exact_artifact_type() -> None:
    assert type(
        create_artifact()
    ) is KnowledgeGovernedRetrievalEvidenceArtifact


def test_artifact_has_exact_slotted_fields() -> None:
    artifact = create_artifact()

    assert tuple(
        field.name
        for field in fields(artifact)
    ) == (
        "payload",
        "digest",
        "media_type",
        "schema_version",
    )
    assert not hasattr(
        artifact,
        "__dict__",
    )


def test_artifact_is_immutable() -> None:
    artifact = create_artifact()

    with pytest.raises(
        FrozenInstanceError,
    ):
        artifact.payload = "{}"


def test_artifact_payload_is_exact_canonical_serialization() -> None:
    evidence = create_mixed_evidence()
    artifact = (
        build_knowledge_governed_retrieval_evidence_artifact(
            evidence=evidence,
        )
    )

    assert artifact.payload == (
        serialize_knowledge_governed_retrieval_evidence(
            evidence=evidence,
        )
    )


def test_artifact_digest_is_exact_content_identity() -> None:
    evidence = create_mixed_evidence()
    artifact = (
        build_knowledge_governed_retrieval_evidence_artifact(
            evidence=evidence,
        )
    )

    assert artifact.digest == (
        digest_knowledge_governed_retrieval_evidence(
            evidence=evidence,
        )
    )


def test_artifact_digest_matches_exact_payload_utf8_bytes() -> None:
    artifact = create_artifact()
    expected = hashlib.sha256(
        artifact.payload.encode("UTF-8")
    ).hexdigest()

    assert artifact.digest.value == expected


def test_artifact_digest_metadata_is_explicit() -> None:
    artifact = create_artifact()

    assert type(
        artifact.digest
    ) is KnowledgeGovernedRetrievalEvidenceDigest
    assert artifact.digest.algorithm == "SHA-256"
    assert artifact.digest.encoding == "UTF-8"


def test_artifact_media_type_is_explicit_and_exact() -> None:
    artifact = create_artifact()

    assert (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_MEDIA_TYPE
        == "application/json"
    )
    assert artifact.media_type == "application/json"


def test_artifact_schema_version_is_explicit_integer() -> None:
    artifact = create_artifact()

    assert artifact.schema_version == (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
    )
    assert artifact.schema_version == 1
    assert type(artifact.schema_version) is int


def test_artifact_is_deterministic_for_same_evidence() -> None:
    evidence = create_mixed_evidence()

    first = build_knowledge_governed_retrieval_evidence_artifact(
        evidence=evidence,
    )
    second = build_knowledge_governed_retrieval_evidence_artifact(
        evidence=evidence,
    )

    assert first == second


def test_equivalent_evidence_produces_identical_artifacts() -> None:
    first = create_artifact()
    second = create_artifact()

    assert first == second


def test_evidence_change_changes_payload_and_digest() -> None:
    baseline = create_artifact(
        raw_text="governed planogram",
    )
    changed = create_artifact(
        raw_text="governed visual manual",
    )

    assert changed.payload != baseline.payload
    assert changed.digest != baseline.digest


def test_artifact_preserves_unicode_payload_bytes() -> None:
    artifact = create_artifact(
        raw_text="Plánograma NIÑAS",
    )

    assert "Plánograma NIÑAS" in artifact.payload
    assert artifact.digest.value == hashlib.sha256(
        artifact.payload.encode("UTF-8")
    ).hexdigest()


def test_artifact_makes_no_authenticity_or_authority_claim() -> None:
    artifact = create_artifact()

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "verified",
        "trust",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            artifact,
            attribute,
        )


def test_builder_introduces_no_received_verification_or_storage() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval_evidence_artifact.py"
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    forbidden_names = {
        "hmac",
        "compare_digest",
        "open",
        "Path",
        "tempfile",
        "replace",
        "unlink",
    }

    assert not (
        forbidden_names
        & {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
    )
    assert "verify_" not in source
    assert "read_text" not in source
    assert "write_text" not in source
