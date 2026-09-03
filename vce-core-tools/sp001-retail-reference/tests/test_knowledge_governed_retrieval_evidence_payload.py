import ast

from pathlib import Path

import pytest

from sp001.services.knowledge_governed_retrieval_evidence_payload import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING,
    canonical_knowledge_governed_retrieval_evidence_payload_bytes,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)
from test_knowledge_governed_retrieval_evidence_serialization import (
    create_evidence,
    create_mixed_evidence,
)


def payload(
    evidence=None,
) -> bytes:
    return (
        canonical_knowledge_governed_retrieval_evidence_payload_bytes(
            evidence=(
                evidence
                if evidence is not None
                else create_mixed_evidence()
            ),
        )
    )


def test_payload_encoding_is_explicit_and_exact() -> None:
    assert (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_ENCODING
        == "UTF-8"
    )


def test_payload_requires_validated_evidence() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        ),
    ):
        canonical_knowledge_governed_retrieval_evidence_payload_bytes(
            evidence="evidence",  # type: ignore[arg-type]
        )


def test_payload_returns_exact_bytes_type() -> None:
    assert type(payload()) is bytes


def test_payload_equals_exact_canonical_serialization_bytes() -> None:
    evidence = create_mixed_evidence()

    assert payload(evidence) == (
        serialize_knowledge_governed_retrieval_evidence(
            evidence=evidence,
        ).encode("UTF-8")
    )


def test_payload_decodes_to_exact_canonical_serialization() -> None:
    evidence = create_mixed_evidence()

    assert payload(evidence).decode(
        "UTF-8"
    ) == serialize_knowledge_governed_retrieval_evidence(
        evidence=evidence,
    )


def test_payload_is_deterministic_for_same_evidence() -> None:
    evidence = create_mixed_evidence()

    assert payload(evidence) == payload(evidence)


def test_equivalent_evidence_produces_identical_bytes() -> None:
    assert payload(
        create_mixed_evidence(),
    ) == payload(
        create_mixed_evidence(),
    )


def test_query_change_changes_payload_bytes() -> None:
    baseline = create_mixed_evidence(
        raw_text="governed planogram",
    )
    changed = create_mixed_evidence(
        raw_text="governed visual manual",
    )

    assert payload(baseline) != payload(changed)


def test_unicode_uses_exact_utf8_bytes() -> None:
    evidence = create_mixed_evidence(
        raw_text="Plánograma NIÑAS",
    )
    observed = payload(evidence)
    expected = (
        serialize_knowledge_governed_retrieval_evidence(
            evidence=evidence,
        ).encode("UTF-8")
    )

    assert observed == expected
    assert "Plánograma NIÑAS".encode("UTF-8") in observed


def test_empty_evidence_has_nonempty_canonical_payload() -> None:
    observed = payload(
        create_evidence(),
    )

    assert observed
    assert b'"candidate_count":0' in observed
    assert b'"candidate_decisions":[]' in observed
    assert b'"entries":[]' in observed


def test_payload_has_no_utf8_byte_order_mark() -> None:
    assert not payload().startswith(
        b"\xef\xbb\xbf"
    )


def test_payload_has_no_trailing_newline() -> None:
    assert not payload().endswith(
        b"\n"
    )


def test_payload_identification_does_not_mutate_evidence() -> None:
    evidence = create_mixed_evidence()
    before = evidence

    payload(evidence)

    assert evidence == before


def test_payload_layer_introduces_no_digest_or_second_json_projection() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval_evidence_payload.py"
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    forbidden_names = {
        "hashlib",
        "sha256",
        "json",
        "dumps",
        "asdict",
        "fields",
        "is_dataclass",
    }

    assert not (
        forbidden_names
        & {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
    )
    assert "digest" not in source
    assert "media_type" not in source
    assert "artifact" not in source
