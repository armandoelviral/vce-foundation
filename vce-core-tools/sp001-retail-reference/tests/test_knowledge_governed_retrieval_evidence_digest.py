import ast
import hashlib
import re

from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from sp001.services.knowledge_governed_retrieval_evidence_digest import (
    KnowledgeGovernedRetrievalEvidenceDigest,
    digest_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    canonical_knowledge_governed_retrieval_evidence_payload_bytes,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_mixed_evidence,
)


def create_digest():
    return digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(),
    )


def test_digest_is_immutable() -> None:
    digest = create_digest()

    with pytest.raises(
        FrozenInstanceError,
    ):
        digest.value = "0" * 64


def test_digest_has_exact_slotted_fields() -> None:
    digest = create_digest()

    assert tuple(
        field.name
        for field in fields(digest)
    ) == (
        "algorithm",
        "encoding",
        "value",
    )
    assert not hasattr(
        digest,
        "__dict__",
    )


def test_digest_declares_sha256_algorithm() -> None:
    assert create_digest().algorithm == "SHA-256"


def test_digest_declares_utf8_encoding() -> None:
    assert create_digest().encoding == "UTF-8"


def test_digest_has_canonical_lowercase_hexadecimal_value() -> None:
    assert re.fullmatch(
        r"[0-9a-f]{64}",
        create_digest().value,
    )


def test_digest_matches_independent_payload_calculation() -> None:
    evidence = create_mixed_evidence()
    expected = hashlib.sha256(
        canonical_knowledge_governed_retrieval_evidence_payload_bytes(
            evidence=evidence,
        )
    ).hexdigest()

    observed = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert observed.value == expected


def test_digest_is_deterministic_for_same_evidence() -> None:
    evidence = create_mixed_evidence()

    first = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )
    second = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert first == second


def test_equivalent_evidence_has_identical_digest() -> None:
    first = digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(),
    )
    second = digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(),
    )

    assert first == second


def test_digest_changes_when_query_changes() -> None:
    baseline = digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(
            raw_text="governed planogram",
        ),
    )
    changed = digest_knowledge_governed_retrieval_evidence(
        evidence=create_mixed_evidence(
            raw_text="governed visual manual",
        ),
    )

    assert changed != baseline


def test_digest_preserves_unicode_utf8_semantics() -> None:
    evidence = create_mixed_evidence(
        raw_text="Plánograma NIÑAS",
    )
    expected = hashlib.sha256(
        canonical_knowledge_governed_retrieval_evidence_payload_bytes(
            evidence=evidence,
        )
    ).hexdigest()

    observed = digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert observed.value == expected


@pytest.mark.parametrize(
    "invalid_evidence",
    (
        None,
        {},
        (),
        "evidence",
    ),
)
def test_digest_rejects_untyped_evidence(
    invalid_evidence: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalEvidence",
    ):
        digest_knowledge_governed_retrieval_evidence(
            evidence=invalid_evidence,
        )


def test_digest_does_not_mutate_evidence() -> None:
    evidence = create_mixed_evidence()
    before = evidence

    digest_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )

    assert evidence == before


def test_digest_makes_no_authenticity_or_authority_claim() -> None:
    digest = create_digest()

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
            digest,
            attribute,
        )


def test_digest_uses_only_canonical_payload_bytes() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval_evidence_digest.py"
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    assert (
        "canonical_knowledge_governed_"
        "retrieval_evidence_payload_bytes"
    ) in source
    assert "serialize_knowledge" not in source
    assert "json.dumps" not in source
    assert not any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "encode"
        for node in ast.walk(tree)
    )
