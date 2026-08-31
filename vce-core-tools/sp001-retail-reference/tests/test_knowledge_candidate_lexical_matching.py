from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_lexical_match import (
    KnowledgeCandidateLexicalMatch,
    KnowledgeLexicalMatchStatus,
    KnowledgeLexicalTermEvidence,
)
from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidate,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
)
from sp001.services.knowledge_candidate_lexical_matching import (
    evaluate_knowledge_candidate_lexical_match,
)
from sp001.services.knowledge_retrieval_manifest import (
    evaluate_knowledge_retrieval_candidates,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)
from test_knowledge_retrieval_manifest import (
    create_binding,
    create_candidate,
    create_candidate_set,
    create_status,
)


def create_query(
    raw_text: str = "governed planogram",
) -> KnowledgeLexicalQuery:
    return KnowledgeLexicalQuery(
        query_id="QUERY-001",
        raw_text=raw_text,
    )


def create_included_candidate(
    *,
    content: bytes = b"governed planogram denim wall",
    candidate_id: str = "CANDIDATE-LEX-001",
    source_id: str = "SOURCE-LEX-001",
) -> KnowledgeRetrievalCandidate:
    source = create_status(
        source_id=source_id,
    )
    source = replace(
        source,
        identity=replace(
            source.identity,
            source_content_digest=(
                digest_knowledge_source_content(
                    content=content,
                )
            ),
        ),
    )

    return KnowledgeRetrievalCandidate(
        candidate_id=candidate_id,
        source_status=source,
        content=content,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=source,
            effective_from=datetime(
                2026,
                3,
                1,
                tzinfo=timezone.utc,
            ),
        ),
        authority_bindings=(
            create_binding(
                source,
            ),
        ),
    )


def candidate_and_decision(
    *,
    content: bytes = b"governed planogram denim wall",
) -> tuple[
    KnowledgeRetrievalCandidate,
    KnowledgeRetrievalCandidateDecision,
]:
    candidate = create_included_candidate(
        content=content,
    )
    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=create_candidate_set(
            candidate,
        ),
    )

    return (
        candidate,
        manifest.candidate_decisions[0],
    )


def create_evidence(
    *,
    index: int,
    term: str,
    count: int,
) -> KnowledgeLexicalTermEvidence:
    return KnowledgeLexicalTermEvidence(
        query_term_index=index,
        term=term,
        occurrence_count=count,
    )


def create_match(
    *,
    query: KnowledgeLexicalQuery | None = None,
    evidence: tuple[
        KnowledgeLexicalTermEvidence,
        ...,
    ] | None = None,
    status: KnowledgeLexicalMatchStatus = (
        KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
    ),
) -> KnowledgeCandidateLexicalMatch:
    selected_query = query or create_query()
    selected_evidence = (
        evidence
        if evidence is not None
        else tuple(
            create_evidence(
                index=index,
                term=term,
                count=1,
            )
            for index, term in enumerate(
                selected_query.terms
            )
        )
    )
    candidate, _ = candidate_and_decision()

    return KnowledgeCandidateLexicalMatch(
        query=selected_query,
        candidate_id=candidate.candidate_id,
        source_identity=candidate.source_status.identity,
        term_evidence=selected_evidence,
        match_status=status,
    )


def evaluate(
    *,
    raw_text: str,
    content: bytes,
) -> KnowledgeCandidateLexicalMatch:
    candidate, decision = candidate_and_decision(
        content=content,
    )

    return evaluate_knowledge_candidate_lexical_match(
        query=create_query(
            raw_text,
        ),
        candidate=candidate,
        candidate_decision=decision,
    )


def test_match_status_vocabulary_is_exact() -> None:
    assert tuple(
        status.value
        for status in KnowledgeLexicalMatchStatus
    ) == (
        "ALL_TERMS_PRESENT",
        "SOME_TERMS_PRESENT",
        "NO_TERMS_PRESENT",
    )


def test_term_evidence_is_immutable() -> None:
    evidence = create_evidence(
        index=0,
        term="denim",
        count=1,
    )

    with pytest.raises(
        FrozenInstanceError,
    ):
        evidence.occurrence_count = 2


def test_term_evidence_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeLexicalTermEvidence
        )
    ) == (
        "query_term_index",
        "term",
        "occurrence_count",
    )


@pytest.mark.parametrize(
    "index",
    (
        True,
        1.0,
        "0",
    ),
)
def test_term_evidence_rejects_untyped_index(
    index: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="query_term_index must be an integer",
    ):
        create_evidence(
            index=index,
            term="denim",
            count=1,
        )


def test_term_evidence_rejects_negative_index() -> None:
    with pytest.raises(
        ValueError,
        match="must not be negative",
    ):
        create_evidence(
            index=-1,
            term="denim",
            count=1,
        )


@pytest.mark.parametrize(
    "term",
    (
        "",
        None,
        1,
    ),
)
def test_term_evidence_rejects_empty_or_untyped_term(
    term: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="term must not be empty",
    ):
        create_evidence(
            index=0,
            term=term,
            count=1,
        )


@pytest.mark.parametrize(
    "count",
    (
        True,
        1.0,
        "1",
    ),
)
def test_term_evidence_rejects_untyped_occurrence_count(
    count: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="occurrence_count must be an integer",
    ):
        create_evidence(
            index=0,
            term="denim",
            count=count,
        )


def test_term_evidence_rejects_negative_occurrence_count() -> None:
    with pytest.raises(
        ValueError,
        match="must not be negative",
    ):
        create_evidence(
            index=0,
            term="denim",
            count=-1,
        )


@pytest.mark.parametrize(
    ("count", "expected"),
    (
        (0, False),
        (1, True),
        (3, True),
    ),
)
def test_term_presence_is_derived_from_occurrence_count(
    count: int,
    expected: bool,
) -> None:
    evidence = create_evidence(
        index=0,
        term="denim",
        count=count,
    )

    assert evidence.is_present is expected


def test_candidate_match_fields_are_exact() -> None:
    assert tuple(
        field.name
        for field in fields(
            KnowledgeCandidateLexicalMatch
        )
    ) == (
        "query",
        "candidate_id",
        "source_identity",
        "term_evidence",
        "match_status",
    )


def test_candidate_match_is_immutable() -> None:
    result = create_match()

    with pytest.raises(
        FrozenInstanceError,
    ):
        result.match_status = (
            KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
        )


def test_candidate_match_rejects_untyped_query() -> None:
    candidate, _ = candidate_and_decision()

    with pytest.raises(
        TypeError,
        match="query must be a KnowledgeLexicalQuery",
    ):
        KnowledgeCandidateLexicalMatch(
            query="query",
            candidate_id=candidate.candidate_id,
            source_identity=candidate.source_status.identity,
            term_evidence=(),
            match_status=(
                KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
            ),
        )


@pytest.mark.parametrize(
    "candidate_id",
    (
        "",
        " ",
        None,
    ),
)
def test_candidate_match_rejects_empty_candidate_id(
    candidate_id: object,
) -> None:
    result = create_match()

    with pytest.raises(
        ValueError,
        match="candidate_id must not be empty",
    ):
        replace(
            result,
            candidate_id=candidate_id,
        )


def test_candidate_match_rejects_untyped_source_identity() -> None:
    result = create_match()

    with pytest.raises(
        TypeError,
        match="source_identity must be",
    ):
        replace(
            result,
            source_identity="SOURCE-001",
        )


def test_candidate_match_requires_immutable_evidence() -> None:
    result = create_match()

    with pytest.raises(
        TypeError,
        match="term_evidence must be an immutable tuple",
    ):
        replace(
            result,
            term_evidence=list(
                result.term_evidence
            ),
        )


def test_candidate_match_requires_every_query_term() -> None:
    result = create_match()

    with pytest.raises(
        ValueError,
        match="must describe every query term",
    ):
        replace(
            result,
            term_evidence=result.term_evidence[:-1],
        )


def test_candidate_match_preserves_query_term_order() -> None:
    result = create_match()

    with pytest.raises(
        ValueError,
        match="must preserve query-term order",
    ):
        replace(
            result,
            term_evidence=(
                replace(
                    result.term_evidence[0],
                    query_term_index=1,
                ),
                result.term_evidence[1],
            ),
        )


def test_candidate_match_requires_query_term_identity() -> None:
    result = create_match()

    with pytest.raises(
        ValueError,
        match="must describe query terms",
    ):
        replace(
            result,
            term_evidence=(
                replace(
                    result.term_evidence[0],
                    term="different",
                ),
                result.term_evidence[1],
            ),
        )


def test_candidate_match_rejects_untyped_status() -> None:
    result = create_match()

    with pytest.raises(
        TypeError,
        match="KnowledgeLexicalMatchStatus",
    ):
        replace(
            result,
            match_status="ALL_TERMS_PRESENT",
        )


def test_candidate_match_status_must_reflect_evidence() -> None:
    query = create_query()

    with pytest.raises(
        ValueError,
        match="must reflect term evidence",
    ):
        create_match(
            query=query,
            evidence=(
                create_evidence(
                    index=0,
                    term=query.terms[0],
                    count=1,
                ),
                create_evidence(
                    index=1,
                    term=query.terms[1],
                    count=0,
                ),
            ),
            status=KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT,
        )


@pytest.mark.parametrize(
    ("query", "candidate", "decision", "message"),
    (
        (
            "query",
            None,
            None,
            "query must be a KnowledgeLexicalQuery",
        ),
        (
            create_query(),
            "candidate",
            None,
            "candidate must be a KnowledgeRetrievalCandidate",
        ),
        (
            create_query(),
            create_included_candidate(),
            "decision",
            "KnowledgeRetrievalCandidateDecision",
        ),
    ),
)
def test_evaluator_rejects_untyped_inputs(
    query: object,
    candidate: object,
    decision: object,
    message: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=message,
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=query,
            candidate=candidate,
            candidate_decision=decision,
        )


def test_evaluator_rejects_candidate_id_mismatch() -> None:
    candidate, decision = candidate_and_decision()
    mismatched = replace(
        candidate,
        candidate_id="CANDIDATE-OTHER",
    )

    with pytest.raises(
        ValueError,
        match="must describe candidate_id",
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=create_query(),
            candidate=mismatched,
            candidate_decision=decision,
        )


def test_evaluator_rejects_source_mismatch() -> None:
    candidate, decision = candidate_and_decision()
    other = create_included_candidate(
        candidate_id=candidate.candidate_id,
        source_id="SOURCE-OTHER",
    )

    with pytest.raises(
        ValueError,
        match="must describe candidate source",
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=create_query(),
            candidate=other,
            candidate_decision=decision,
        )


def test_evaluator_blocks_excluded_candidate() -> None:
    candidate = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )
    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=create_candidate_set(
            candidate,
        ),
    )

    with pytest.raises(
        ValueError,
        match="requires an INCLUDED decision",
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=create_query(),
            candidate=candidate,
            candidate_decision=manifest.candidate_decisions[0],
        )


def test_evaluator_rejects_inconsistent_included_decision() -> None:
    candidate, record = candidate_and_decision()
    inconsistent = replace(
        record,
        decision=replace(
            record.decision,
            content_bytes_match_digest=False,
        ),
    )

    assert inconsistent.decision.decision_status is (
        KnowledgeRetrievalDecisionStatus.INCLUDED
    )

    with pytest.raises(
        ValueError,
        match="must verify candidate content bytes",
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=create_query(),
            candidate=candidate,
            candidate_decision=inconsistent,
        )


def test_all_query_terms_present_are_explained() -> None:
    result = evaluate(
        raw_text="denim wall",
        content=b"denim wall denim presentation",
    )

    assert result.match_status is (
        KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
    )
    assert tuple(
        evidence.occurrence_count
        for evidence in result.term_evidence
    ) == (
        2,
        1,
    )


def test_some_query_terms_present_are_explained() -> None:
    result = evaluate(
        raw_text="denim fixture",
        content=b"denim wall presentation",
    )

    assert result.match_status is (
        KnowledgeLexicalMatchStatus.SOME_TERMS_PRESENT
    )
    assert tuple(
        evidence.occurrence_count
        for evidence in result.term_evidence
    ) == (
        1,
        0,
    )


def test_no_query_terms_present_are_explained() -> None:
    result = evaluate(
        raw_text="fixture table",
        content=b"denim wall presentation",
    )

    assert result.match_status is (
        KnowledgeLexicalMatchStatus.NO_TERMS_PRESENT
    )
    assert tuple(
        evidence.occurrence_count
        for evidence in result.term_evidence
    ) == (
        0,
        0,
    )


def test_duplicate_query_terms_preserve_separate_evidence() -> None:
    result = evaluate(
        raw_text="denim denim",
        content=b"denim wall denim",
    )

    assert tuple(
        (
            evidence.query_term_index,
            evidence.term,
            evidence.occurrence_count,
        )
        for evidence in result.term_evidence
    ) == (
        (0, "denim", 2),
        (1, "denim", 2),
    )


def test_matching_uses_shared_unicode_normalization() -> None:
    result = evaluate(
        raw_text="STRASSE denim",
        content="Straße ＤＥＮＩＭ".encode(
            "UTF-8"
        ),
    )

    assert result.match_status is (
        KnowledgeLexicalMatchStatus.ALL_TERMS_PRESENT
    )


def test_matching_preserves_complete_punctuation_tokens() -> None:
    result = evaluate(
        raw_text="denim, wall",
        content=b"denim wall denim,",
    )

    assert tuple(
        evidence.occurrence_count
        for evidence in result.term_evidence
    ) == (
        1,
        1,
    )


def test_matching_rejects_invalid_utf8() -> None:
    candidate, decision = candidate_and_decision(
        content=b"\xff\xfe",
    )

    with pytest.raises(
        UnicodeDecodeError,
    ):
        evaluate_knowledge_candidate_lexical_match(
            query=create_query(),
            candidate=candidate,
            candidate_decision=decision,
        )


def test_match_result_grants_no_ranking_or_relevance_claim() -> None:
    names = {
        field.name
        for field in fields(
            KnowledgeCandidateLexicalMatch
        )
    }

    assert "score" not in names
    assert "rank" not in names
    assert "ranking" not in names
    assert "relevance" not in names
    assert "semantic_relevance" not in names
