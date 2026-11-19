"""Pure commercial approval scope coverage; no authority is granted."""

from sp001.contracts.knowledge_source_scope import (
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)


def selection_covers(
    grant: KnowledgeScopeSelection,
    requested: KnowledgeScopeSelection,
) -> bool:
    if not isinstance(grant, KnowledgeScopeSelection):
        raise TypeError("invalid grant selection")
    if not isinstance(requested, KnowledgeScopeSelection):
        raise TypeError("invalid requested selection")

    if grant.mode is KnowledgeScopeMode.ALL:
        return True

    if requested.mode is KnowledgeScopeMode.ALL:
        return False

    return set(requested.ids).issubset(grant.ids)


def commercial_scope_covers(
    grant: KnowledgeSourceScope,
    requested: KnowledgeSourceScope,
) -> bool:
    if not isinstance(grant, KnowledgeSourceScope):
        raise TypeError("invalid grant scope")
    if not isinstance(requested, KnowledgeSourceScope):
        raise TypeError("invalid requested scope")

    if (
        grant.organization_id != requested.organization_id
        or grant.customer_id != requested.customer_id
        or grant.jurisdiction != requested.jurisdiction
        or grant.commercial_channel_id != requested.commercial_channel_id
        or grant.document_type != requested.document_type
    ):
        return False

    if (
        grant.campaign_id is not None
        and grant.campaign_id != requested.campaign_id
    ):
        return False

    return (
        selection_covers(
            grant.point_of_sale_scope,
            requested.point_of_sale_scope,
        )
        and selection_covers(
            grant.department_scope,
            requested.department_scope,
        )
    )
