import ast

from pathlib import Path

import pytest

from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
    digest_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_digest_verification import (
    verify_knowledge_governed_retrieval_evidence_digest,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def test_verification_accepts_matching_digest() -> None:
    evidence = create_mixed_evidence()
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert verify_knowledge_governed_retrieval_evidence_digest(
        evidence=evidence,
        digest=digest,
    )


def test_verification_accepts_equivalent_evidence() -> None:
    original = create_mixed_evidence()
    equivalent = create_mixed_evidence()
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=original,
    )

    assert original is not equivalent
    assert verify_knowledge_governed_retrieval_evidence_digest(
        evidence=equivalent,
        digest=digest,
    )


def test_verification_rejects_nonmatching_content() -> None:
    original = create_mixed_evidence(
        raw_text="governed planogram",
    )
    changed = create_mixed_evidence(
        raw_text="governed visual manual",
    )
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=original,
    )

    assert not verify_knowledge_governed_retrieval_evidence_digest(
        evidence=changed,
        digest=digest,
    )


@pytest.mark.parametrize(
    "invalid_evidence",
    (
        None,
        {},
        (),
        "evidence",
    ),
)
def test_verification_rejects_untyped_evidence(
    invalid_evidence: object,
) -> None:
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(),
    )

    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidence",
    ):
        verify_knowledge_governed_retrieval_evidence_digest(
            evidence=invalid_evidence,
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_digest",
    (
        None,
        {},
        (),
        "digest",
    ),
)
def test_verification_rejects_untyped_digest(
    invalid_digest: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidenceDigest",
    ):
        verify_knowledge_governed_retrieval_evidence_digest(
            evidence=create_mixed_evidence(),
            digest=invalid_digest,
        )


def test_verification_rejects_unsupported_algorithm() -> None:
    digest = KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm="SHA-512",
        encoding="UTF-8",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match="algorithm must be SHA-256",
    ):
        verify_knowledge_governed_retrieval_evidence_digest(
            evidence=create_mixed_evidence(),
            digest=digest,
        )


def test_verification_rejects_unsupported_encoding() -> None:
    digest = KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm="SHA-256",
        encoding="UTF-16",
        value="0" * 64,
    )

    with pytest.raises(
        ValueError,
        match="encoding must be UTF-8",
    ):
        verify_knowledge_governed_retrieval_evidence_digest(
            evidence=create_mixed_evidence(),
            digest=digest,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        None,
        "",
        "0" * 63,
        "0" * 65,
        "G" * 64,
        "A" * 64,
        123,
    ),
)
def test_verification_rejects_invalid_digest_value(
    invalid_value: object,
) -> None:
    digest = KnowledgeGovernedRetrievalEvidenceDigest(
        algorithm="SHA-256",
        encoding="UTF-8",
        value=invalid_value,
    )

    with pytest.raises(
        ValueError,
        match="64 lowercase hexadecimal characters",
    ):
        verify_knowledge_governed_retrieval_evidence_digest(
            evidence=create_mixed_evidence(),
            digest=digest,
        )


def test_verification_returns_exact_boolean() -> None:
    evidence = create_mixed_evidence()
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    result = verify_knowledge_governed_retrieval_evidence_digest(
        evidence=evidence,
        digest=digest,
    )

    assert result is True


def test_verification_uses_constant_time_comparison() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / (
            "knowledge_governed_retrieval_evidence_"
            "digest_verification.py"
        )
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "compare_digest"
        for node in ast.walk(tree)
    )
    assert "hmac.compare_digest" in source


def test_verification_does_not_mutate_inputs() -> None:
    evidence = create_mixed_evidence()
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )
    evidence_before = evidence
    digest_before = digest

    verify_knowledge_governed_retrieval_evidence_digest(
        evidence=evidence,
        digest=digest,
    )

    assert evidence == evidence_before
    assert digest == digest_before


def test_success_establishes_no_authenticity_or_authority() -> None:
    evidence = create_mixed_evidence()
    digest = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert verify_knowledge_governed_retrieval_evidence_digest(
        evidence=evidence,
        digest=digest,
    )

    for attribute in (
        "signature",
        "signer",
        "authenticity",
        "authority",
        "approved",
        "legal_status",
        "customer_acceptance",
    ):
        assert not hasattr(
            digest,
            attribute,
        )


def test_verification_recomputes_declared_content_identity() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / (
            "knowledge_governed_retrieval_evidence_"
            "digest_verification.py"
        )
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )

    assert (
        "digest_knowledge_governed_retrieval_evidence"
        in source
    )
    assert "serialize_knowledge" not in source
    assert "payload.encode" not in source
