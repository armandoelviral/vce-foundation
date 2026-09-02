import ast

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_lexical_query,
    project_knowledge_retrieval_context,
)


def create_query(
    raw_text: str = "governed planogram",
) -> KnowledgeLexicalQuery:
    return KnowledgeLexicalQuery(
        query_id="QUERY-001",
        raw_text=raw_text,
    )


def create_context(
    *,
    campaign_id: str | None = "CAMPAIGN-001",
    evaluated_at: datetime | None = None,
) -> KnowledgeRetrievalContext:
    return KnowledgeRetrievalContext(
        organization_id="ORG-001",
        customer_id="CUSTOMER-001",
        jurisdiction="MX",
        commercial_channel_id="RETAIL",
        document_type=KnowledgeDocumentType.VISUAL_MANUAL,
        point_of_sale_id="POS-001",
        department_id="CHILDRENS",
        campaign_id=campaign_id,
        evaluated_at=(
            evaluated_at
            if evaluated_at is not None
            else datetime(
                2026,
                3,
                15,
                12,
                0,
                tzinfo=timezone.utc,
            )
        ),
    )


def test_query_projection_requires_validated_query() -> None:
    with pytest.raises(
        TypeError,
        match="query must be a KnowledgeLexicalQuery",
    ):
        project_knowledge_lexical_query(
            query="query",  # type: ignore[arg-type]
        )


def test_context_projection_requires_validated_context() -> None:
    with pytest.raises(
        TypeError,
        match="context must be a KnowledgeRetrievalContext",
    ):
        project_knowledge_retrieval_context(
            context="context",  # type: ignore[arg-type]
        )


def test_query_projection_has_exact_fields() -> None:
    document = project_knowledge_lexical_query(
        query=create_query(),
    )

    assert set(document) == {
        "query_id",
        "raw_text",
        "normalized_text",
        "terms",
        "normalization_policy",
    }


def test_query_projection_preserves_identity_and_raw_text() -> None:
    document = project_knowledge_lexical_query(
        query=create_query("  governed   planogram  "),
    )

    assert document["query_id"] == "QUERY-001"
    assert document["raw_text"] == "  governed   planogram  "


def test_query_projection_preserves_normalized_text() -> None:
    document = project_knowledge_lexical_query(
        query=create_query("  Plánograma   NIÑAS  "),
    )

    assert document["normalized_text"] == "plánograma niñas"


def test_query_projection_preserves_declared_term_order() -> None:
    document = project_knowledge_lexical_query(
        query=create_query("second first second"),
    )

    assert document["terms"] == [
        "second",
        "first",
        "second",
    ]


def test_query_projection_preserves_normalization_policy() -> None:
    query = create_query()
    document = project_knowledge_lexical_query(
        query=query,
    )

    assert (
        document["normalization_policy"]
        == query.normalization_policy
    )


def test_query_projection_uses_json_compatible_term_list() -> None:
    document = project_knowledge_lexical_query(
        query=create_query(),
    )

    assert type(document["terms"]) is list


def test_context_projection_has_exact_fields() -> None:
    document = project_knowledge_retrieval_context(
        context=create_context(),
    )

    assert set(document) == {
        "organization_id",
        "customer_id",
        "jurisdiction",
        "commercial_channel_id",
        "document_type",
        "point_of_sale_id",
        "department_id",
        "campaign_id",
        "evaluated_at",
    }


def test_context_projection_preserves_scope_values() -> None:
    document = project_knowledge_retrieval_context(
        context=create_context(),
    )

    assert document == {
        "organization_id": "ORG-001",
        "customer_id": "CUSTOMER-001",
        "jurisdiction": "MX",
        "commercial_channel_id": "RETAIL",
        "document_type": "VISUAL_MANUAL",
        "point_of_sale_id": "POS-001",
        "department_id": "CHILDRENS",
        "campaign_id": "CAMPAIGN-001",
        "evaluated_at": "2026-03-15T12:00:00+00:00",
    }


def test_context_projection_uses_enum_value() -> None:
    document = project_knowledge_retrieval_context(
        context=create_context(),
    )

    assert (
        document["document_type"]
        == KnowledgeDocumentType.VISUAL_MANUAL.value
    )


def test_context_projection_preserves_absent_campaign() -> None:
    document = project_knowledge_retrieval_context(
        context=create_context(
            campaign_id=None,
        ),
    )

    assert document["campaign_id"] is None


def test_context_projection_preserves_declared_utc_offset() -> None:
    offset = timezone(
        timedelta(
            hours=-6,
        )
    )
    document = project_knowledge_retrieval_context(
        context=create_context(
            evaluated_at=datetime(
                2026,
                3,
                15,
                6,
                30,
                tzinfo=offset,
            ),
        ),
    )

    assert document["evaluated_at"] == (
        "2026-03-15T06:30:00-06:00"
    )


def test_projection_uses_no_generic_or_premature_serialization() -> None:
    source_path = (
        Path(__file__).parents[1]
        / "src"
        / "sp001"
        / "services"
        / (
            "knowledge_governed_retrieval_"
            "query_context_projection.py"
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
        "json",
        "hashlib",
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
    assert "digest" not in source
