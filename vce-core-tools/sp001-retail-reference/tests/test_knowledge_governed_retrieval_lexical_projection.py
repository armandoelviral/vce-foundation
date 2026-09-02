import ast

from pathlib import Path

import pytest

from sp001.services.knowledge_governed_retrieval_lexical_projection import (
    project_knowledge_lexical_ordering,
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


def create_ordering(
    *,
    raw_text: str = "governed planogram",
):
    return execute(
        create_included_candidate(
            candidate_id="CANDIDATE-STRONG",
            source_id="SOURCE-STRONG",
            content=b"governed governed planogram",
        ),
        create_included_candidate(
            candidate_id="CANDIDATE-NONE",
            source_id="SOURCE-NONE",
            content=b"unrelated content",
        ),
        raw_text=raw_text,
    ).lexical_ordering


def project(
    *,
    raw_text: str = "governed planogram",
):
    return project_knowledge_lexical_ordering(
        ordering=create_ordering(
            raw_text=raw_text,
        ),
    )


def test_projection_requires_validated_ordering() -> None:
    with pytest.raises(
        TypeError,
        match="ordering must be a KnowledgeLexicalOrdering",
    ):
        project_knowledge_lexical_ordering(
            ordering="ordering",  # type: ignore[arg-type]
        )


def test_ordering_projection_has_exact_root_fields() -> None:
    assert set(project()) == {
        "query",
        "entries",
        "ordering_policy",
    }


def test_empty_ordering_preserves_empty_entry_universe() -> None:
    ordering = execute().lexical_ordering
    document = project_knowledge_lexical_ordering(
        ordering=ordering,
    )

    assert document["entries"] == []


def test_ordering_query_uses_shared_projection() -> None:
    ordering = create_ordering()
    document = project_knowledge_lexical_ordering(
        ordering=ordering,
    )

    assert document["query"] == (
        project_knowledge_lexical_query(
            query=ordering.query,
        )
    )


def test_ordered_entries_preserve_materialized_order() -> None:
    document = project()

    assert [
        entry["evidence"]["match"]["candidate_id"]
        for entry in document["entries"]
    ] == [
        "CANDIDATE-STRONG",
        "CANDIDATE-NONE",
    ]


def test_ordering_policy_is_preserved_exactly() -> None:
    ordering = create_ordering()
    document = project_knowledge_lexical_ordering(
        ordering=ordering,
    )

    assert document["ordering_policy"] == (
        ordering.ordering_policy
    )


def test_ordering_entry_has_exact_fields() -> None:
    entry = project()["entries"][0]

    assert set(entry) == {
        "declared_candidate_index",
        "ordered_candidate_index",
        "evidence",
    }


def test_declared_and_ordered_indexes_are_preserved() -> None:
    ordering = create_ordering()
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"]

    assert [
        (
            entry["declared_candidate_index"],
            entry["ordered_candidate_index"],
        )
        for entry in projected
    ] == [
        (
            entry.declared_candidate_index,
            entry.ordered_candidate_index,
        )
        for entry in ordering.entries
    ]


def test_ordering_evidence_has_exact_fields() -> None:
    evidence = project()["entries"][0]["evidence"]

    assert set(evidence) == {
        "match",
        "status_precedence",
        "present_query_term_count",
        "total_occurrence_count",
        "ordering_key",
        "ordering_policy",
    }


def test_ordering_counts_and_policy_are_preserved() -> None:
    ordering = create_ordering()
    source = ordering.entries[0].evidence
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"][0]["evidence"]

    assert projected["status_precedence"] == (
        source.status_precedence
    )
    assert projected["present_query_term_count"] == (
        source.present_query_term_count
    )
    assert projected["total_occurrence_count"] == (
        source.total_occurrence_count
    )
    assert projected["ordering_policy"] == (
        source.ordering_policy
    )


def test_ordering_key_uses_json_compatible_list() -> None:
    ordering = create_ordering()
    source = ordering.entries[0].evidence
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"][0]["evidence"]

    assert projected["ordering_key"] == list(
        source.ordering_key
    )
    assert type(projected["ordering_key"]) is list


def test_match_projection_has_exact_fields() -> None:
    match = project()["entries"][0]["evidence"]["match"]

    assert set(match) == {
        "query",
        "candidate_id",
        "source_identity",
        "term_evidence",
        "match_status",
    }


def test_match_source_identity_and_digest_are_complete() -> None:
    ordering = create_ordering()
    identity = (
        ordering.entries[0]
        .evidence.match.source_identity
    )
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"][0]["evidence"]["match"][
        "source_identity"
    ]

    assert projected == {
        "source_id": identity.source_id,
        "source_version": identity.source_version,
        "source_content_digest": {
            "algorithm": (
                identity.source_content_digest.algorithm
            ),
            "value": identity.source_content_digest.value,
        },
    }


def test_term_evidence_has_exact_fields() -> None:
    term = project()["entries"][0]["evidence"][
        "match"
    ]["term_evidence"][0]

    assert set(term) == {
        "query_term_index",
        "term",
        "occurrence_count",
    }


def test_term_positions_and_counts_are_preserved() -> None:
    ordering = create_ordering()
    source = (
        ordering.entries[0]
        .evidence.match.term_evidence
    )
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"][0]["evidence"]["match"][
        "term_evidence"
    ]

    assert [
        (
            term["query_term_index"],
            term["term"],
            term["occurrence_count"],
        )
        for term in projected
    ] == [
        (
            term.query_term_index,
            term.term,
            term.occurrence_count,
        )
        for term in source
    ]


def test_duplicate_query_terms_remain_position_specific() -> None:
    document = project(
        raw_text="governed governed planogram",
    )
    terms = document["entries"][0]["evidence"][
        "match"
    ]["term_evidence"]

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


def test_match_status_uses_declared_enum_value() -> None:
    ordering = create_ordering()
    projected = project_knowledge_lexical_ordering(
        ordering=ordering,
    )["entries"]

    assert [
        entry["evidence"]["match"]["match_status"]
        for entry in projected
    ] == [
        entry.evidence.match.match_status.value
        for entry in ordering.entries
    ]


def test_projection_contains_only_json_compatible_values() -> None:
    document = project(
        raw_text="governed governed planogram",
    )

    def assert_compatible(value) -> None:
        if isinstance(
            value,
            dict,
        ):
            assert all(
                isinstance(key, str)
                for key in value
            )
            for nested in value.values():
                assert_compatible(nested)
            return
        if isinstance(
            value,
            list,
        ):
            for nested in value:
                assert_compatible(nested)
            return
        assert value is None or type(value) in {
            str,
            int,
            bool,
        }

    assert_compatible(document)


def test_projection_uses_no_generic_or_premature_serialization() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval_lexical_projection.py"
    )
    source = source_path.read_text(
        encoding="UTF-8",
    )
    tree = ast.parse(source)

    forbidden_names = {
        "asdict",
        "fields",
        "is_dataclass",
        "json",
        "hashlib",
        "sorted",
    }

    assert not (
        forbidden_names
        & {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
        }
    )
    assert "serialize" not in source
    assert "digest_knowledge_governed" not in source
