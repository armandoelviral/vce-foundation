import ast
from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

from sp001.contracts.knowledge_lexical_match import (
    KnowledgeLexicalMatchStatus,
)
from sp001.contracts.knowledge_lexical_ordering import (
    KnowledgeLexicalOrdering,
    KnowledgeLexicalOrderingEntry,
)
from sp001.contracts.knowledge_lexical_ordering_evidence import (
    KNOWLEDGE_LEXICAL_ORDERING_POLICY,
    KnowledgeCandidateLexicalOrderingEvidence,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.services.knowledge_lexical_ordering import (
    order_knowledge_candidate_lexical_evidence,
)
from sp001.services.knowledge_lexical_ordering_evidence import (
    materialize_knowledge_candidate_lexical_ordering_evidence,
)
from test_knowledge_candidate_lexical_matching import (
    create_evidence,
    create_match,
    create_query,
)


def create_ordering_evidence(
    *,
    query: KnowledgeLexicalQuery,
    counts: tuple[int, ...],
    identity_number: int,
) -> KnowledgeCandidateLexicalOrderingEvidence:
    term_evidence = tuple(
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
    base_match = create_match(
        query=query,
        evidence=term_evidence,
        status=status,
    )
    distinct_match = replace(
        base_match,
        candidate_id=f"CANDIDATE-ORDER-{identity_number:03d}",
        source_identity=replace(
            base_match.source_identity,
            source_id=f"SOURCE-ORDER-{identity_number:03d}",
        ),
    )

    return (
        materialize_knowledge_candidate_lexical_ordering_evidence(
            match=distinct_match,
        )
    )


def order(
    *,
    query: KnowledgeLexicalQuery,
    evidence: tuple[
        KnowledgeCandidateLexicalOrderingEvidence,
        ...,
    ],
) -> KnowledgeLexicalOrdering:
    return order_knowledge_candidate_lexical_evidence(
        query=query,
        evidence=evidence,
    )


def test_ordering_reuses_exact_versioned_policy() -> None:
    result = order(
        query=create_query(),
        evidence=(),
    )

    assert result.ordering_policy == (
        KNOWLEDGE_LEXICAL_ORDERING_POLICY
    )


def test_empty_evidence_produces_empty_ordering() -> None:
    query = create_query()

    result = order(
        query=query,
        evidence=(),
    )

    assert result.query == query
    assert result.entries == ()


def test_ordering_requires_typed_query() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeLexicalQuery",
    ):
        order_knowledge_candidate_lexical_evidence(
            query=object(),
            evidence=(),
        )


def test_ordering_requires_immutable_evidence_tuple() -> None:
    with pytest.raises(
        TypeError,
        match="immutable tuple",
    ):
        order_knowledge_candidate_lexical_evidence(
            query=create_query(),
            evidence=[],
        )


def test_ordering_requires_typed_evidence_values() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeCandidateLexicalOrderingEvidence",
    ):
        order(
            query=create_query(),
            evidence=(
                object(),
            ),
        )


def test_all_evidence_must_use_exact_ordering_query() -> None:
    query = create_query()
    other_query = create_query(
        "different query",
    )
    candidate = create_ordering_evidence(
        query=other_query,
        counts=(1, 1),
        identity_number=1,
    )

    with pytest.raises(
        ValueError,
        match="must use ordering query",
    ):
        order(
            query=query,
            evidence=(
                candidate,
            ),
        )


def test_status_precedence_is_primary_ordering_dimension() -> None:
    query = create_query()
    none = create_ordering_evidence(
        query=query,
        counts=(0, 0),
        identity_number=1,
    )
    some = create_ordering_evidence(
        query=query,
        counts=(100, 0),
        identity_number=2,
    )
    all_terms = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=3,
    )

    result = order(
        query=query,
        evidence=(
            none,
            some,
            all_terms,
        ),
    )

    assert tuple(
        entry.evidence
        for entry in result.entries
    ) == (
        all_terms,
        some,
        none,
    )


def test_coverage_precedes_total_occurrence_count() -> None:
    query = create_query(
        "one two three",
    )
    one_present = create_ordering_evidence(
        query=query,
        counts=(100, 0, 0),
        identity_number=1,
    )
    two_present = create_ordering_evidence(
        query=query,
        counts=(1, 1, 0),
        identity_number=2,
    )

    result = order(
        query=query,
        evidence=(
            one_present,
            two_present,
        ),
    )

    assert tuple(
        entry.evidence
        for entry in result.entries
    ) == (
        two_present,
        one_present,
    )


def test_frequency_orders_equal_status_and_coverage() -> None:
    query = create_query()
    lower = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )
    higher = create_ordering_evidence(
        query=query,
        counts=(4, 2),
        identity_number=2,
    )

    result = order(
        query=query,
        evidence=(
            lower,
            higher,
        ),
    )

    assert tuple(
        entry.evidence
        for entry in result.entries
    ) == (
        higher,
        lower,
    )


def test_exact_ties_preserve_declared_candidate_order() -> None:
    query = create_query()
    first = create_ordering_evidence(
        query=query,
        counts=(2, 1),
        identity_number=1,
    )
    second = create_ordering_evidence(
        query=query,
        counts=(2, 1),
        identity_number=2,
    )
    third = create_ordering_evidence(
        query=query,
        counts=(2, 1),
        identity_number=3,
    )

    result = order(
        query=query,
        evidence=(
            first,
            second,
            third,
        ),
    )

    assert tuple(
        entry.evidence
        for entry in result.entries
    ) == (
        first,
        second,
        third,
    )


def test_entries_record_declared_and_resulting_positions() -> None:
    query = create_query()
    lower = create_ordering_evidence(
        query=query,
        counts=(1, 0),
        identity_number=1,
    )
    higher = create_ordering_evidence(
        query=query,
        counts=(3, 3),
        identity_number=2,
    )

    result = order(
        query=query,
        evidence=(
            lower,
            higher,
        ),
    )

    assert tuple(
        (
            entry.declared_candidate_index,
            entry.ordered_candidate_index,
        )
        for entry in result.entries
    ) == (
        (
            1,
            0,
        ),
        (
            0,
            1,
        ),
    )


def test_duplicate_query_positions_retain_weight_in_ordering() -> None:
    query = create_query(
        "planogram planogram",
    )
    lower = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )
    higher = create_ordering_evidence(
        query=query,
        counts=(3, 3),
        identity_number=2,
    )

    result = order(
        query=query,
        evidence=(
            lower,
            higher,
        ),
    )

    assert result.entries[0].evidence == higher
    assert higher.total_occurrence_count == 6


def test_duplicate_candidate_identity_is_rejected() -> None:
    query = create_query()
    first = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )
    duplicate = replace(
        create_ordering_evidence(
            query=query,
            counts=(2, 2),
            identity_number=2,
        ),
        match=replace(
            create_ordering_evidence(
                query=query,
                counts=(2, 2),
                identity_number=2,
            ).match,
            candidate_id=first.match.candidate_id,
        ),
    )

    with pytest.raises(
        ValueError,
        match="duplicate candidate_id",
    ):
        order(
            query=query,
            evidence=(
                first,
                duplicate,
            ),
        )


def test_duplicate_source_identity_is_rejected() -> None:
    query = create_query()
    first = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )
    second = create_ordering_evidence(
        query=query,
        counts=(2, 2),
        identity_number=2,
    )
    duplicate = replace(
        second,
        match=replace(
            second.match,
            source_identity=first.match.source_identity,
        ),
    )

    with pytest.raises(
        ValueError,
        match="duplicate candidate source identity",
    ):
        order(
            query=query,
            evidence=(
                first,
                duplicate,
            ),
        )


def test_contract_rejects_noncontiguous_declared_indexes() -> None:
    query = create_query()
    evidence = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )

    with pytest.raises(
        ValueError,
        match="declared_candidate_index values",
    ):
        KnowledgeLexicalOrdering(
            query=query,
            entries=(
                KnowledgeLexicalOrderingEntry(
                    declared_candidate_index=2,
                    ordered_candidate_index=0,
                    evidence=evidence,
                ),
            ),
        )


def test_contract_rejects_incorrect_ordered_index() -> None:
    query = create_query()
    evidence = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )

    with pytest.raises(
        ValueError,
        match="ordered_candidate_index",
    ):
        KnowledgeLexicalOrdering(
            query=query,
            entries=(
                KnowledgeLexicalOrderingEntry(
                    declared_candidate_index=0,
                    ordered_candidate_index=1,
                    evidence=evidence,
                ),
            ),
        )


def test_contract_rejects_unstable_equal_key_order() -> None:
    query = create_query()
    first = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=1,
    )
    second = create_ordering_evidence(
        query=query,
        counts=(1, 1),
        identity_number=2,
    )

    with pytest.raises(
        ValueError,
        match="preserve declared candidate order",
    ):
        KnowledgeLexicalOrdering(
            query=query,
            entries=(
                KnowledgeLexicalOrderingEntry(
                    declared_candidate_index=1,
                    ordered_candidate_index=0,
                    evidence=second,
                ),
                KnowledgeLexicalOrderingEntry(
                    declared_candidate_index=0,
                    ordered_candidate_index=1,
                    evidence=first,
                ),
            ),
        )


def test_ordering_contracts_are_frozen() -> None:
    result = order(
        query=create_query(),
        evidence=(),
    )

    with pytest.raises(FrozenInstanceError):
        result.entries = ()


def test_public_contract_fields_are_exact() -> None:
    assert tuple(
        value.name
        for value in fields(
            KnowledgeLexicalOrderingEntry
        )
    ) == (
        "declared_candidate_index",
        "ordered_candidate_index",
        "evidence",
    )
    assert tuple(
        value.name
        for value in fields(
            KnowledgeLexicalOrdering
        )
    ) == (
        "query",
        "entries",
        "ordering_policy",
    )


def test_ordering_service_does_not_reevaluate_content_or_governance() -> None:
    service_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_lexical_ordering.py"
    )
    source = ast.parse(
        service_path.read_text(
            encoding="UTF-8",
        )
    )
    imports = {
        alias.name
        for node in ast.walk(source)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    attributes = {
        node.attr
        for node in ast.walk(source)
        if isinstance(node, ast.Attribute)
    }

    assert "KnowledgeRetrievalCandidate" not in imports
    assert "KnowledgeRetrievalCandidateDecision" not in imports
    assert "KnowledgeRetrievalManifest" not in imports
    assert "content" not in attributes
    assert "decision" not in attributes
