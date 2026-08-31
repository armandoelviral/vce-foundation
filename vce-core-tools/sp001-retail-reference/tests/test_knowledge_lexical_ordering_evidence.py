import ast
from pathlib import Path
from dataclasses import FrozenInstanceError, fields

import pytest

from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
    KnowledgeLexicalMatchStatus,
)
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KNOWLEDGE_LEXICAL_ORDERING_POLICY,
    KnowledgeCandidateLexicalOrderingEvidence,
)
from sp001.services.knowledge_lexical_ordering_evidence import (
    materialize_knowledge_candidate_lexical_ordering_evidence,
)
from test_knowledge_candidate_lexical_matching import (
    create_evidence,
    create_match,
    create_query,
)


def materialize(
    *,
    raw_text: str = "governed planogram",
    counts: tuple[int, ...] = (1, 1),
) -> KnowledgeCandidateLexicalOrderingEvidence:
    query = create_query(
        raw_text,
    )
    evidence = tuple(
        create_evidence(
            index=index,
            term=term,
            count=counts[index],
        )
        for index, term in enumerate(
            query.terms
        )
    )
    present_count = sum(
        count > 0
        for count in counts
    )
    status = (
        KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
        if present_count == len(counts)
        else (
            KnowledgeLexicalMatchStatus.SOME_TERMS_PRESENT
            if present_count
            else KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
        )
    )

    return (
        materialize_knowledge_candidate_lexical_ordering_evidence(
            match=create_match(
                query=query,
                evidence=evidence,
                status=status,
            ),
        )
    )


def test_ordering_policy_identifier_is_explicit_and_versioned() -> None:
    assert KNOWLEDGE_LEXICAL_ORDERING_POLICY == (
        "MATCH_STATUS_PRESENT_QUERY_TERMS_TOTAL_OCCURRENCES_V1"
    )


def test_materializer_requires_typed_match() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeCandidateLexicalMatch",
    ):
        materialize_knowledge_candidate_lexical_ordering_evidence(
            match=object(),
        )


def test_contract_requires_typed_match() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeCandidateLexicalMatch",
    ):
        KnowledgeCandidateLexicalOrderingEvidence(
            match=object(),
        )


def test_all_terms_present_has_highest_status_precedence() -> None:
    evidence = materialize(
        counts=(1, 1),
    )

    assert evidence.status_precedence == 2
    assert evidence.present_query_term_count == 2
    assert evidence.total_occurrence_count == 2
    assert evidence.ordering_key == (
        2,
        2,
        2,
    )


def test_some_terms_present_has_intermediate_precedence() -> None:
    evidence = materialize(
        counts=(4, 0),
    )

    assert evidence.status_precedence == 1
    assert evidence.present_query_term_count == 1
    assert evidence.total_occurrence_count == 4
    assert evidence.ordering_key == (
        1,
        1,
        4,
    )


def test_no_terms_present_has_lowest_precedence() -> None:
    evidence = materialize(
        counts=(0, 0),
    )

    assert evidence.status_precedence == 0
    assert evidence.present_query_term_count == 0
    assert evidence.total_occurrence_count == 0
    assert evidence.ordering_key == (
        0,
        0,
        0,
    )


def test_duplicate_query_positions_retain_declared_weight() -> None:
    evidence = materialize(
        raw_text="planogram planogram",
        counts=(3, 3),
    )

    assert evidence.present_query_term_count == 2
    assert evidence.total_occurrence_count == 6
    assert evidence.ordering_key == (
        2,
        2,
        6,
    )


def test_total_occurrences_are_aggregated_after_coverage() -> None:
    lower_frequency = materialize(
        counts=(1, 1),
    )
    higher_frequency = materialize(
        counts=(5, 2),
    )

    assert lower_frequency.ordering_key == (
        2,
        2,
        2,
    )
    assert higher_frequency.ordering_key == (
        2,
        2,
        7,
    )


def test_materialization_is_deterministic() -> None:
    match = materialize(
        counts=(2, 1),
    ).match

    first = materialize_knowledge_candidate_lexical_ordering_evidence(
        match=match,
    )
    second = materialize_knowledge_candidate_lexical_ordering_evidence(
        match=match,
    )

    assert first == second


def test_ordering_key_contains_no_candidate_identity_tiebreaker() -> None:
    evidence = materialize(
        counts=(2, 1),
    )

    assert evidence.match.candidate_id
    assert evidence.match.source_identity
    assert evidence.ordering_key == (
        2,
        2,
        3,
    )
    assert all(
        isinstance(value, int)
        for value in evidence.ordering_key
    )


def test_ordering_evidence_is_frozen() -> None:
    evidence = materialize()

    with pytest.raises(FrozenInstanceError):
        evidence.total_occurrence_count = 99


def test_ordering_evidence_uses_slots() -> None:
    evidence = materialize()

    assert not hasattr(
        evidence,
        "__dict__",
    )


def test_public_field_surface_is_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeCandidateLexicalOrderingEvidence
        )
    ) == (
        "match",
        "status_precedence",
        "present_query_term_count",
        "total_occurrence_count",
        "ordering_key",
        "ordering_policy",
    )


def test_derived_fields_cannot_be_supplied_by_caller() -> None:
    match = materialize().match

    with pytest.raises(TypeError):
        KnowledgeCandidateLexicalOrderingEvidence(
            match=match,
            status_precedence=99,
        )


def test_lex003a_performs_no_sorting_or_content_evaluation() -> None:
    service_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_lexical_ordering_evidence.py"
    )
    source = ast.parse(
        service_path.read_text(
            encoding="UTF-8",
        )
    )
    names = {
        node.id
        for node in ast.walk(source)
        if isinstance(node, ast.Name)
    }
    attributes = {
        node.attr
        for node in ast.walk(source)
        if isinstance(node, ast.Attribute)
    }
    imports = {
        alias.name
        for node in ast.walk(source)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }

    assert "sorted" not in names
    assert "sort" not in attributes
    assert "KnowledgeRetrievalCandidate" not in imports
    assert "KnowledgeRetrievalCandidateDecision" not in imports
    assert "content" not in attributes
