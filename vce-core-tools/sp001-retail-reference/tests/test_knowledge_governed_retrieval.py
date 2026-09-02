import ast
from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval import (
    KnowledgeGovernedRetrievalResult,
)
from sp001.contracts.knowledge_lexical_match import (
    KnowledgeLexicalMatchStatus,
)
from sp001.contracts.knowledge_lexical_ordering import (
    KnowledgeLexicalOrdering,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.services.knowledge_governed_retrieval import (
    execute_governed_knowledge_retrieval,
)
from test_knowledge_candidate_lexical_matching import (
    create_included_candidate,
    create_query,
)
from test_knowledge_retrieval_manifest import (
    create_candidate,
    create_candidate_set,
)


def execute(
    *candidates,
    raw_text: str = "governed planogram",
) -> KnowledgeGovernedRetrievalResult:
    return execute_governed_knowledge_retrieval(
        query=create_query(
            raw_text,
        ),
        candidate_set=create_candidate_set(
            *candidates,
        ),
    )


def test_empty_candidate_universe_produces_complete_empty_result() -> None:
    result = execute()

    assert result.manifest.candidate_decisions == ()
    assert result.lexical_ordering.entries == ()
    assert result.included_candidate_decisions == ()
    assert result.excluded_candidate_decisions == ()
    assert result.ordered_candidate_ids == ()


def test_executor_requires_typed_query() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeLexicalQuery",
    ):
        execute_governed_knowledge_retrieval(
            query=object(),
            candidate_set=create_candidate_set(),
        )


def test_executor_requires_typed_candidate_set() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeRetrievalCandidateSet",
    ):
        execute_governed_knowledge_retrieval(
            query=create_query(),
            candidate_set=object(),
        )


def test_result_preserves_complete_manifest_order() -> None:
    included = create_included_candidate(
        candidate_id="CANDIDATE-INCLUDED",
        source_id="SOURCE-INCLUDED",
    )
    excluded = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )

    result = execute(
        included,
        excluded,
    )

    assert tuple(
        record.candidate_id
        for record in result.manifest.candidate_decisions
    ) == (
        "CANDIDATE-INCLUDED",
        "CANDIDATE-EXCLUDED",
    )


def test_only_governance_included_candidates_are_matched() -> None:
    included = create_included_candidate(
        candidate_id="CANDIDATE-INCLUDED",
        source_id="SOURCE-INCLUDED",
    )
    excluded = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )

    result = execute(
        excluded,
        included,
    )

    assert result.ordered_candidate_ids == (
        "CANDIDATE-INCLUDED",
    )
    assert tuple(
        record.candidate_id
        for record in result.excluded_candidate_decisions
    ) == (
        "CANDIDATE-EXCLUDED",
    )


def test_excluded_invalid_utf8_is_not_lexically_decoded() -> None:
    excluded = replace(
        create_candidate(
            candidate_id="CANDIDATE-EXCLUDED",
            source_id="SOURCE-EXCLUDED",
            included=False,
        ),
        content=b"\xff",
    )

    result = execute(
        excluded,
    )

    assert result.ordered_candidate_ids == ()
    assert len(
        result.excluded_candidate_decisions
    ) == 1


def test_included_invalid_utf8_blocks_complete_execution() -> None:
    included = create_included_candidate(
        content=b"\xff",
        candidate_id="CANDIDATE-INCLUDED",
        source_id="SOURCE-INCLUDED",
    )

    with pytest.raises(
        UnicodeDecodeError,
    ):
        execute(
            included,
        )


def test_lexical_policy_orders_all_included_candidates() -> None:
    lower = create_included_candidate(
        content=b"governed other",
        candidate_id="CANDIDATE-LOWER",
        source_id="SOURCE-LOWER",
    )
    higher = create_included_candidate(
        content=b"governed governed planogram planogram",
        candidate_id="CANDIDATE-HIGHER",
        source_id="SOURCE-HIGHER",
    )

    result = execute(
        lower,
        higher,
    )

    assert result.ordered_candidate_ids == (
        "CANDIDATE-HIGHER",
        "CANDIDATE-LOWER",
    )


def test_no_term_matches_remain_visible_when_governance_included() -> None:
    candidate = create_included_candidate(
        content=b"unrelated lexical content",
        candidate_id="CANDIDATE-NONE",
        source_id="SOURCE-NONE",
    )

    result = execute(
        candidate,
    )

    assert result.ordered_candidate_ids == (
        "CANDIDATE-NONE",
    )
    assert (
        result.lexical_ordering.entries[
            0
        ].evidence.match.match_status
        is KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
    )


def test_exact_lexical_ties_preserve_included_declared_order() -> None:
    first = create_included_candidate(
        content=b"governed planogram",
        candidate_id="CANDIDATE-FIRST",
        source_id="SOURCE-FIRST",
    )
    excluded = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )
    second = create_included_candidate(
        content=b"governed planogram",
        candidate_id="CANDIDATE-SECOND",
        source_id="SOURCE-SECOND",
    )

    result = execute(
        first,
        excluded,
        second,
    )

    assert result.ordered_candidate_ids == (
        "CANDIDATE-FIRST",
        "CANDIDATE-SECOND",
    )
    assert tuple(
        entry.declared_candidate_index
        for entry in result.lexical_ordering.entries
    ) == (
        0,
        1,
    )


def test_ordered_identity_matches_manifest_decision_identity() -> None:
    candidate = create_included_candidate(
        candidate_id="CANDIDATE-001",
        source_id="SOURCE-001",
    )

    result = execute(
        candidate,
    )

    entry = result.lexical_ordering.entries[0]
    record = result.included_candidate_decisions[0]

    assert (
        entry.evidence.match.source_identity
        == record.decision.source_status.identity
    )


def test_manifest_context_is_candidate_set_context() -> None:
    candidate_set = create_candidate_set()
    query = create_query()

    result = execute_governed_knowledge_retrieval(
        query=query,
        candidate_set=candidate_set,
    )

    assert (
        result.manifest.retrieval_context
        == candidate_set.retrieval_context
    )


def test_execution_is_deterministic() -> None:
    candidate = create_included_candidate(
        candidate_id="CANDIDATE-001",
        source_id="SOURCE-001",
    )
    candidate_set = create_candidate_set(
        candidate,
    )
    query = create_query()

    first = execute_governed_knowledge_retrieval(
        query=query,
        candidate_set=candidate_set,
    )
    second = execute_governed_knowledge_retrieval(
        query=query,
        candidate_set=candidate_set,
    )

    assert first == second


def test_result_rejects_query_mismatch() -> None:
    first_query = create_query()
    second_query = create_query(
        "different query",
    )

    with pytest.raises(
        ValueError,
        match="must use result query",
    ):
        KnowledgeGovernedRetrievalResult(
            query=first_query,
            manifest=execute().manifest,
            lexical_ordering=KnowledgeLexicalOrdering(
                query=second_query,
                entries=(),
            ),
        )


def test_result_rejects_missing_included_candidate() -> None:
    candidate = create_included_candidate(
        candidate_id="CANDIDATE-001",
        source_id="SOURCE-001",
    )
    complete = execute(
        candidate,
    )

    with pytest.raises(
        ValueError,
        match="every and only included",
    ):
        KnowledgeGovernedRetrievalResult(
            query=complete.query,
            manifest=complete.manifest,
            lexical_ordering=KnowledgeLexicalOrdering(
                query=complete.query,
                entries=(),
            ),
        )


def test_result_is_frozen() -> None:
    result = execute()

    with pytest.raises(FrozenInstanceError):
        result.manifest = execute().manifest


def test_result_public_fields_are_exact() -> None:
    assert tuple(
        value.name
        for value in fields(
            KnowledgeGovernedRetrievalResult
        )
    ) == (
        "query",
        "manifest",
        "lexical_ordering",
    )


def test_execution_does_not_mutate_inputs() -> None:
    candidate = create_included_candidate(
        candidate_id="CANDIDATE-001",
        source_id="SOURCE-001",
    )
    candidate_set = create_candidate_set(
        candidate,
    )
    before = candidate_set

    execute_governed_knowledge_retrieval(
        query=create_query(),
        candidate_set=candidate_set,
    )

    assert candidate_set == before


def test_service_introduces_no_threshold_or_semantic_selection() -> None:
    service_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / "knowledge_governed_retrieval.py"
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

    assert "threshold" not in names
    assert "limit" not in names
    assert "score" not in attributes
    assert "relevance" not in attributes
