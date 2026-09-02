from sp001.contracts.knowledge_lexical_query import (
    KnowledgeLexicalQuery,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)


def project_knowledge_lexical_query(
    *,
    query: KnowledgeLexicalQuery,
) -> dict[str, object]:
    """Project one validated lexical query without inference."""

    if not isinstance(
        query,
        KnowledgeLexicalQuery,
    ):
        raise TypeError(
            "query must be a KnowledgeLexicalQuery"
        )

    return {
        "query_id": query.query_id,
        "raw_text": query.raw_text,
        "normalized_text": query.normalized_text,
        "terms": list(query.terms),
        "normalization_policy": query.normalization_policy,
    }


def project_knowledge_retrieval_context(
    *,
    context: KnowledgeRetrievalContext,
) -> dict[str, object]:
    """Project one validated retrieval context exactly."""

    if not isinstance(
        context,
        KnowledgeRetrievalContext,
    ):
        raise TypeError(
            "context must be a KnowledgeRetrievalContext"
        )

    return {
        "organization_id": context.organization_id,
        "customer_id": context.customer_id,
        "jurisdiction": context.jurisdiction,
        "commercial_channel_id": (
            context.commercial_channel_id
        ),
        "document_type": context.document_type.value,
        "point_of_sale_id": context.point_of_sale_id,
        "department_id": context.department_id,
        "campaign_id": context.campaign_id,
        "evaluated_at": context.evaluated_at.isoformat(),
    }
