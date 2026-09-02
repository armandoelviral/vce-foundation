import ast
import json

from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
    KnowledgeGovernedRetrievalEvidence,
)
from sp001.services.knowledge_governed_retrieval_evidence_serialization import (
    serialize_knowledge_governed_retrieval_evidence,
)
from sp001.services.knowledge_governed_retrieval_lexical_projection import (
    project_knowledge_lexical_ordering,
)
from sp001.services.knowledge_governed_retrieval_manifest_projection import (
    project_knowledge_retrieval_manifest,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_lexical_query,
)
from test_knowledge_candidate_lexical_matching import (
    create_included_candidate,
)
from test_knowledge_governed_retrieval import (
    execute,
)
from test_knowledge_retrieval_manifest import (
    create_candidate,
)


def create_evidence(
    *candidates,
    raw_text: str = "governed planogram",
) -> KnowledgeGovernedRetrievalEvidence:
    return KnowledgeGovernedRetrievalEvidence(
        result=execute(
            *candidates,
            raw_text=raw_text,
        ),
    )


def create_mixed_evidence(
    *,
    raw_text: str = "governed planogram",
) -> KnowledgeGovernedRetrievalEvidence:
    return create_evidence(
        create_included_candidate(
            candidate_id="CANDIDATE-INCLUDED",
            source_id="SOURCE-INCLUDED",
            content=b"governed governed planogram",
        ),
        create_candidate(
            candidate_id="CANDIDATE-EXCLUDED",
            source_id="SOURCE-EXCLUDED",
            included=False,
        ),
        raw_text=raw_text,
    )


def serialize(
    evidence: KnowledgeGovernedRetrievalEvidence | None = None,
) -> str:
    return serialize_knowledge_governed_retrieval_evidence(
        evidence=(
            evidence
            if evidence is not None
            else create_mixed_evidence()
        ),
    )


def test_serializer_requires_validated_evidence() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evidence must be a "
            "KnowledgeGovernedRetrievalEvidence"
        ),
    ):
        serialize_knowledge_governed_retrieval_evidence(
            evidence="evidence",  # type: ignore[arg-type]
        )


def test_serializer_returns_text() -> None:
    assert type(serialize()) is str


def test_payload_contains_json_object() -> None:
    assert isinstance(
        json.loads(
            serialize()
        ),
        dict,
    )


def test_payload_has_exact_root_fields() -> None:
    assert set(
        json.loads(
            serialize()
        )
    ) == {
        "schema_version",
        "counts",
        "result",
    }


def test_schema_version_is_explicit_exact_integer() -> None:
    document = json.loads(
        serialize()
    )

    assert (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
        == 1
    )
    assert document["schema_version"] == 1
    assert type(document["schema_version"]) is int


def test_reconciliation_counts_are_complete_and_exact() -> None:
    evidence = create_mixed_evidence()
    counts = json.loads(
        serialize(
            evidence,
        )
    )["counts"]

    assert counts == {
        "candidate_count": evidence.candidate_count,
        "included_candidate_count": (
            evidence.included_candidate_count
        ),
        "excluded_candidate_count": (
            evidence.excluded_candidate_count
        ),
        "ordered_candidate_count": (
            evidence.ordered_candidate_count
        ),
    }
    assert all(
        type(value) is int
        for value in counts.values()
    )


def test_empty_evidence_preserves_empty_universes() -> None:
    document = json.loads(
        serialize(
            create_evidence(),
        )
    )

    assert document["counts"] == {
        "candidate_count": 0,
        "included_candidate_count": 0,
        "excluded_candidate_count": 0,
        "ordered_candidate_count": 0,
    }
    assert (
        document["result"]["manifest"]["candidate_decisions"]
        == []
    )
    assert (
        document["result"]["lexical_ordering"]["entries"]
        == []
    )


def test_result_query_uses_verified_query_projection() -> None:
    evidence = create_mixed_evidence()
    document = json.loads(
        serialize(
            evidence,
        )
    )

    assert document["result"]["query"] == (
        project_knowledge_lexical_query(
            query=evidence.result.query,
        )
    )


def test_result_manifest_uses_verified_manifest_projection() -> None:
    evidence = create_mixed_evidence()
    document = json.loads(
        serialize(
            evidence,
        )
    )

    assert document["result"]["manifest"] == (
        project_knowledge_retrieval_manifest(
            manifest=evidence.result.manifest,
        )
    )


def test_result_ordering_uses_verified_lexical_projection() -> None:
    evidence = create_mixed_evidence()
    document = json.loads(
        serialize(
            evidence,
        )
    )

    assert document["result"]["lexical_ordering"] == (
        project_knowledge_lexical_ordering(
            ordering=evidence.result.lexical_ordering,
        )
    )


def test_payload_preserves_included_and_excluded_decisions() -> None:
    candidates = json.loads(
        serialize()
    )["result"]["manifest"]["candidate_decisions"]

    assert [
        (
            candidate["candidate_id"],
            candidate["decision"]["decision_status"],
        )
        for candidate in candidates
    ] == [
        (
            "CANDIDATE-INCLUDED",
            "INCLUDED",
        ),
        (
            "CANDIDATE-EXCLUDED",
            "EXCLUDED",
        ),
    ]


def test_serializer_is_deterministic_for_same_evidence() -> None:
    evidence = create_mixed_evidence()

    assert serialize(
        evidence,
    ) == serialize(
        evidence,
    )


def test_equivalent_evidence_produces_identical_payload() -> None:
    assert serialize(
        create_mixed_evidence(),
    ) == serialize(
        create_mixed_evidence(),
    )


def test_candidate_order_changes_payload() -> None:
    included = create_included_candidate(
        candidate_id="CANDIDATE-INCLUDED",
        source_id="SOURCE-INCLUDED",
        content=b"governed planogram",
    )
    excluded = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )

    first = create_evidence(
        included,
        excluded,
    )
    second = create_evidence(
        excluded,
        included,
    )

    assert serialize(first) != serialize(second)


def test_unicode_is_preserved_without_ascii_escaping() -> None:
    payload = serialize(
        create_mixed_evidence(
            raw_text="Plánograma NIÑAS",
        ),
    )

    assert "Plánograma NIÑAS" in payload
    assert "plánograma niñas" in payload
    assert "\\u00e1" not in payload
    assert "\\u00d1" not in payload


def test_payload_uses_compact_json_separators() -> None:
    payload = serialize()

    assert ": " not in payload
    assert ", " not in payload
    assert "\n" not in payload


def test_payload_uses_canonical_sorted_keys() -> None:
    payload = serialize()
    document = json.loads(
        payload
    )

    assert payload == json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def test_duplicate_terms_and_positions_remain_explicit() -> None:
    document = json.loads(
        serialize(
            create_mixed_evidence(
                raw_text="governed governed planogram",
            ),
        )
    )
    terms = document["result"]["lexical_ordering"][
        "entries"
    ][0]["evidence"]["match"]["term_evidence"]

    assert [
        (
            term["query_term_index"],
            term["term"],
        )
        for term in terms
    ] == [
        (0, "governed"),
        (1, "governed"),
        (2, "planogram"),
    ]


def test_serializer_introduces_no_digest_or_artifact_claim() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / (
            "knowledge_governed_retrieval_"
            "evidence_serialization.py"
        )
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    forbidden_names = {
        "asdict",
        "fields",
        "is_dataclass",
        "hashlib",
        "datetime",
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
