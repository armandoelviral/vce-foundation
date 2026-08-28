from dataclasses import FrozenInstanceError

import pytest

from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)


def all_scope() -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.ALL,
        ids=(),
    )


def explicit_scope(
    *ids: str,
) -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.EXPLICIT,
        ids=tuple(ids),
    )


def create_scope(
    **overrides: object,
) -> KnowledgeSourceScope:
    values = {
        "organization_id": "RETAIL-GROUP-GLOBAL",
        "customer_id": "BRAND-CASUAL-X",
        "jurisdiction": "MX",
        "commercial_channel_id": "PHYSICAL_STORE",
        "document_type": KnowledgeDocumentType.PLANOGRAM,
        "point_of_sale_scope": explicit_scope(
            "POS-012",
            "POS-045",
            "POS-089",
        ),
        "department_scope": explicit_scope(
            "DPT-DENIM",
            "DPT-MENSWEAR",
        ),
        "campaign_id": "CAMP-SPRING-2026",
    }
    values.update(overrides)

    return KnowledgeSourceScope(
        **values,
    )


def test_document_type_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeDocumentType) == (
        KnowledgeDocumentType.VISUAL_MANUAL,
        KnowledgeDocumentType.PLANOGRAM,
        KnowledgeDocumentType.LOOKBOOK,
        KnowledgeDocumentType.BUSINESS_RULE,
        KnowledgeDocumentType.SAFETY_GUIDELINE,
    )


def test_scope_mode_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeScopeMode) == (
        KnowledgeScopeMode.ALL,
        KnowledgeScopeMode.EXPLICIT,
    )


def test_all_scope_preserves_explicit_universal_semantics() -> None:
    selection = all_scope()

    assert selection.mode is KnowledgeScopeMode.ALL
    assert selection.ids == ()


def test_explicit_scope_preserves_ordered_identities() -> None:
    selection = explicit_scope(
        "POS-012",
        "POS-045",
    )

    assert selection.mode is KnowledgeScopeMode.EXPLICIT
    assert selection.ids == (
        "POS-012",
        "POS-045",
    )


def test_scope_selection_is_immutable() -> None:
    selection = all_scope()

    with pytest.raises(FrozenInstanceError):
        selection.ids = (
            "POS-001",
        )


def test_scope_selection_rejects_untyped_mode() -> None:
    with pytest.raises(
        TypeError,
        match="mode must be a KnowledgeScopeMode",
    ):
        KnowledgeScopeSelection(
            mode="ALL",
            ids=(),
        )


def test_scope_selection_rejects_mutable_ids() -> None:
    with pytest.raises(
        TypeError,
        match="ids must be an immutable tuple",
    ):
        KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.EXPLICIT,
            ids=[
                "POS-001",
            ],
        )


@pytest.mark.parametrize(
    "invalid_id",
    (
        "",
        " ",
        None,
        123,
    ),
)
def test_scope_selection_rejects_empty_identities(
    invalid_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="scoped id must not be empty",
    ):
        KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.EXPLICIT,
            ids=(
                invalid_id,
            ),
        )


def test_scope_selection_rejects_duplicate_identities() -> None:
    with pytest.raises(
        ValueError,
        match="duplicate scoped id: POS-001",
    ):
        explicit_scope(
            "POS-001",
            "POS-001",
        )


def test_all_scope_rejects_explicit_identities() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "ALL scope must not declare explicit ids"
        ),
    ):
        KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.ALL,
            ids=(
                "POS-001",
            ),
        )


def test_explicit_scope_rejects_empty_identity_collection() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "EXPLICIT scope requires at least one id"
        ),
    ):
        KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.EXPLICIT,
            ids=(),
        )


def test_knowledge_source_scope_preserves_all_dimensions() -> None:
    scope = create_scope()

    assert scope.organization_id == (
        "RETAIL-GROUP-GLOBAL"
    )
    assert scope.customer_id == "BRAND-CASUAL-X"
    assert scope.jurisdiction == "MX"
    assert scope.commercial_channel_id == (
        "PHYSICAL_STORE"
    )
    assert scope.document_type is (
        KnowledgeDocumentType.PLANOGRAM
    )
    assert scope.point_of_sale_scope.ids == (
        "POS-012",
        "POS-045",
        "POS-089",
    )
    assert scope.department_scope.ids == (
        "DPT-DENIM",
        "DPT-MENSWEAR",
    )
    assert scope.campaign_id == "CAMP-SPRING-2026"


def test_campaign_can_remain_undeclared() -> None:
    scope = create_scope(
        campaign_id=None,
    )

    assert scope.campaign_id is None


@pytest.mark.parametrize(
    "field, value",
    (
        ("organization_id", ""),
        ("customer_id", " "),
        ("jurisdiction", None),
        ("commercial_channel_id", 123),
    ),
)
def test_knowledge_source_scope_rejects_empty_identity(
    field: str,
    value: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_scope(
            **{
                field: value,
            },
        )


def test_knowledge_source_scope_rejects_untyped_document() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "document_type must be a "
            "KnowledgeDocumentType"
        ),
    ):
        create_scope(
            document_type="PLANOGRAM",
        )


@pytest.mark.parametrize(
    "field",
    (
        "point_of_sale_scope",
        "department_scope",
    ),
)
def test_knowledge_source_scope_rejects_untyped_selection(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=(
            f"{field} must be a "
            "KnowledgeScopeSelection"
        ),
    ):
        create_scope(
            **{
                field: (
                    "POS-001",
                ),
            },
        )


@pytest.mark.parametrize(
    "invalid_campaign",
    (
        "",
        " ",
        123,
    ),
)
def test_campaign_rejects_empty_declared_identity(
    invalid_campaign: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "campaign_id must not be empty "
            "when declared"
        ),
    ):
        create_scope(
            campaign_id=invalid_campaign,
        )


def test_knowledge_source_scope_is_immutable() -> None:
    scope = create_scope()

    with pytest.raises(FrozenInstanceError):
        scope.customer_id = "BRAND-OTHER"


def test_same_retail_scope_remains_distinct_across_customers() -> None:
    scope_a = create_scope(
        customer_id="CUSTOMER-A",
    )
    scope_b = create_scope(
        customer_id="CUSTOMER-B",
    )

    assert (
        scope_a.point_of_sale_scope
        == scope_b.point_of_sale_scope
    )
    assert scope_a != scope_b


def test_scope_does_not_claim_lifecycle_evidence_or_authority() -> None:
    scope = create_scope()

    for attribute in (
        "lifecycle_status",
        "evidence_status",
        "authority_status",
        "authority_source_id",
        "approved",
        "effective_from",
        "effective_until",
        "applicable",
    ):
        assert not hasattr(
            scope,
            attribute,
        )
