from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
    KnowledgeScopeMatchStatus,
    KnowledgeScopeMismatchReason,
    KnowledgeSourceScopeEvaluation,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)


def evaluate_knowledge_source_scope(
    *,
    source_scope: KnowledgeSourceScope,
    retrieval_context: KnowledgeRetrievalContext,
) -> KnowledgeSourceScopeEvaluation:
    """Compare every declared scope dimension deterministically."""

    if not isinstance(source_scope, KnowledgeSourceScope):
        raise TypeError(
            "source_scope must be a KnowledgeSourceScope"
        )

    if not isinstance(
        retrieval_context,
        KnowledgeRetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a "
            "KnowledgeRetrievalContext"
        )

    reasons: list[KnowledgeScopeMismatchReason] = []

    if (
        source_scope.organization_id
        != retrieval_context.organization_id
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.ORGANIZATION_MISMATCH
        )

    if (
        source_scope.customer_id
        != retrieval_context.customer_id
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH
        )

    if (
        source_scope.jurisdiction
        != retrieval_context.jurisdiction
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.JURISDICTION_MISMATCH
        )

    if (
        source_scope.commercial_channel_id
        != retrieval_context.commercial_channel_id
    ):
        reasons.append(
            KnowledgeScopeMismatchReason
            .COMMERCIAL_CHANNEL_MISMATCH
        )

    if (
        source_scope.document_type
        is not retrieval_context.document_type
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.DOCUMENT_TYPE_MISMATCH
        )

    if not _selection_matches(
        selection=source_scope.point_of_sale_scope,
        contextual_id=retrieval_context.point_of_sale_id,
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.POINT_OF_SALE_MISMATCH
        )

    if not _selection_matches(
        selection=source_scope.department_scope,
        contextual_id=retrieval_context.department_id,
    ):
        reasons.append(
            KnowledgeScopeMismatchReason.DEPARTMENT_MISMATCH
        )

    if source_scope.campaign_id != retrieval_context.campaign_id:
        reasons.append(
            KnowledgeScopeMismatchReason.CAMPAIGN_MISMATCH
        )

    mismatch_reasons = tuple(reasons)

    if mismatch_reasons:
        match_status = (
            KnowledgeScopeMatchStatus.DOES_NOT_MATCH
        )
    else:
        match_status = KnowledgeScopeMatchStatus.MATCHES

    return KnowledgeSourceScopeEvaluation(
        source_scope=source_scope,
        retrieval_context=retrieval_context,
        match_status=match_status,
        mismatch_reasons=mismatch_reasons,
    )


def _selection_matches(
    *,
    selection: KnowledgeScopeSelection,
    contextual_id: str,
) -> bool:
    if selection.mode is KnowledgeScopeMode.ALL:
        return True

    return contextual_id in selection.ids
