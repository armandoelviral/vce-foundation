import ast
from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from sp001.contracts.knowledge_governed_retrieval_evidence import (
    KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION,
    KnowledgeGovernedRetrievalEvidence,
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


def test_schema_version_is_explicit_and_exact() -> None:
    assert (
        KNOWLEDGE_GOVERNED_RETRIEVAL_EVIDENCE_SCHEMA_VERSION
        == 1
    )


def test_evidence_requires_typed_governed_result() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeGovernedRetrievalResult",
    ):
        KnowledgeGovernedRetrievalEvidence(
            result=object(),
        )


def test_empty_result_has_reconciled_zero_counts() -> None:
    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(),
    )

    assert evidence.schema_version == 1
    assert evidence.candidate_count == 0
    assert evidence.included_candidate_count == 0
    assert evidence.excluded_candidate_count == 0
    assert evidence.ordered_candidate_count == 0


def test_mixed_result_has_reconciled_counts() -> None:
    included = create_included_candidate(
        candidate_id="CANDIDATE-INCLUDED",
        source_id="SOURCE-INCLUDED",
    )
    excluded = create_candidate(
        candidate_id="CANDIDATE-EXCLUDED",
        source_id="SOURCE-EXCLUDED",
        included=False,
    )

    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(
            included,
            excluded,
        ),
    )

    assert evidence.candidate_count == 2
    assert evidence.included_candidate_count == 1
    assert evidence.excluded_candidate_count == 1
    assert evidence.ordered_candidate_count == 1


def test_multiple_included_candidates_reconcile_with_ordering() -> None:
    first = create_included_candidate(
        candidate_id="CANDIDATE-FIRST",
        source_id="SOURCE-FIRST",
    )
    second = create_included_candidate(
        candidate_id="CANDIDATE-SECOND",
        source_id="SOURCE-SECOND",
    )

    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(
            first,
            second,
        ),
    )

    assert evidence.candidate_count == 2
    assert evidence.included_candidate_count == 2
    assert evidence.excluded_candidate_count == 0
    assert evidence.ordered_candidate_count == 2


def test_no_term_match_remains_counted_when_governance_included() -> None:
    candidate = create_included_candidate(
        content=b"unrelated content",
        candidate_id="CANDIDATE-NONE",
        source_id="SOURCE-NONE",
    )

    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(
            candidate,
        ),
    )

    assert evidence.included_candidate_count == 1
    assert evidence.ordered_candidate_count == 1


def test_evidence_preserves_exact_governed_result() -> None:
    result = execute()

    evidence = KnowledgeGovernedRetrievalEvidence(
        result=result,
    )

    assert evidence.result is result


def test_schema_version_cannot_be_supplied_by_caller() -> None:
    with pytest.raises(TypeError):
        KnowledgeGovernedRetrievalEvidence(
            result=execute(),
            schema_version=2,
        )


def test_derived_counts_cannot_be_supplied_by_caller() -> None:
    with pytest.raises(TypeError):
        KnowledgeGovernedRetrievalEvidence(
            result=execute(),
            candidate_count=99,
        )


def test_count_values_are_exact_integers() -> None:
    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(),
    )

    assert type(
        evidence.candidate_count
    ) is int
    assert type(
        evidence.included_candidate_count
    ) is int
    assert type(
        evidence.excluded_candidate_count
    ) is int
    assert type(
        evidence.ordered_candidate_count
    ) is int


def test_evidence_is_frozen() -> None:
    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(),
    )

    with pytest.raises(FrozenInstanceError):
        evidence.candidate_count = 99


def test_evidence_uses_slots() -> None:
    evidence = KnowledgeGovernedRetrievalEvidence(
        result=execute(),
    )

    assert not hasattr(
        evidence,
        "__dict__",
    )


def test_public_field_surface_is_exact() -> None:
    assert tuple(
        value.name
        for value in fields(
            KnowledgeGovernedRetrievalEvidence
        )
    ) == (
        "result",
        "schema_version",
        "candidate_count",
        "included_candidate_count",
        "excluded_candidate_count",
        "ordered_candidate_count",
    )


def test_art001_introduces_no_wire_or_digest_capability() -> None:
    contract_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "contracts"
        / "knowledge_governed_retrieval_evidence.py"
    )
    tree = ast.parse(
        contract_path.read_text(
            encoding="UTF-8",
        )
    )
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    function_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    assert "json" not in imports
    assert "hashlib" not in imports
    assert "datetime" not in imported_names
    assert "serialize" not in function_names
    assert "digest" not in function_names
