from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
    KnowledgeScopeMatchStatus,
    KnowledgeScopeMismatchReason,
    KnowledgeSourceScopeEvaluation,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.services.knowledge_source_scope_matching import (
    evaluate_knowledge_source_scope,
)


EVALUATED_AT = datetime(
    2026,
    3,
    15,
    12,
    0,
    tzinfo=timezone.utc,
)


def explicit(*ids: str) -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.EXPLICIT,
        ids=tuple(ids),
    )


def all_values() -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.ALL,
        ids=(),
    )


def create_scope(
    **overrides: object,
) -> KnowledgeSourceScope:
    values: dict[str, object] = {
        "organization_id": "ORG-001",
        "customer_id": "CUSTOMER-001",
        "jurisdiction": "MX",
        "commercial_channel_id": "PHYSICAL-STORE",
        "document_type": KnowledgeDocumentType.PLANOGRAM,
        "point_of_sale_scope": explicit(
            "POS-045",
            "POS-089",
        ),
        "department_scope": explicit(
            "DPT-DENIM",
            "DPT-MENSWEAR",
        ),
        "campaign_id": "CAMP-SPRING-2026",
    }
    values.update(overrides)
    return KnowledgeSourceScope(**values)


def create_context(
    **overrides: object,
) -> KnowledgeRetrievalContext:
    values: dict[str, object] = {
        "organization_id": "ORG-001",
        "customer_id": "CUSTOMER-001",
        "jurisdiction": "MX",
        "commercial_channel_id": "PHYSICAL-STORE",
        "document_type": KnowledgeDocumentType.PLANOGRAM,
        "point_of_sale_id": "POS-045",
        "department_id": "DPT-DENIM",
        "campaign_id": "CAMP-SPRING-2026",
        "evaluated_at": EVALUATED_AT,
    }
    values.update(overrides)
    return KnowledgeRetrievalContext(**values)


def evaluate(
    *,
    scope: KnowledgeSourceScope | None = None,
    context: KnowledgeRetrievalContext | None = None,
) -> KnowledgeSourceScopeEvaluation:
    return evaluate_knowledge_source_scope(
        source_scope=scope or create_scope(),
        retrieval_context=context or create_context(),
    )


def test_match_status_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeScopeMatchStatus) == (
        KnowledgeScopeMatchStatus.MATCHES,
        KnowledgeScopeMatchStatus.DOES_NOT_MATCH,
    )


def test_mismatch_reason_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeScopeMismatchReason) == (
        KnowledgeScopeMismatchReason.ORGANIZATION_MISMATCH,
        KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH,
        KnowledgeScopeMismatchReason.JURISDICTION_MISMATCH,
        (
            KnowledgeScopeMismatchReason
            .COMMERCIAL_CHANNEL_MISMATCH
        ),
        KnowledgeScopeMismatchReason.DOCUMENT_TYPE_MISMATCH,
        KnowledgeScopeMismatchReason.POINT_OF_SALE_MISMATCH,
        KnowledgeScopeMismatchReason.DEPARTMENT_MISMATCH,
        KnowledgeScopeMismatchReason.CAMPAIGN_MISMATCH,
    )


def test_context_preserves_explicit_retrieval_dimensions() -> None:
    context = create_context()

    assert context.point_of_sale_id == "POS-045"
    assert context.department_id == "DPT-DENIM"
    assert context.evaluated_at == EVALUATED_AT


@pytest.mark.parametrize(
    "field",
    (
        "organization_id",
        "customer_id",
        "jurisdiction",
        "commercial_channel_id",
        "point_of_sale_id",
        "department_id",
    ),
)
def test_context_rejects_empty_identity(
    field: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{field} must not be empty",
    ):
        create_context(**{field: " "})


def test_context_rejects_untyped_document_type() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeDocumentType",
    ):
        create_context(document_type="PLANOGRAM")


def test_context_rejects_empty_declared_campaign() -> None:
    with pytest.raises(
        ValueError,
        match="campaign_id must not be empty",
    ):
        create_context(campaign_id="")


def test_context_accepts_undeclared_campaign() -> None:
    context = create_context(campaign_id=None)

    assert context.campaign_id is None


def test_context_requires_timezone_aware_instant() -> None:
    with pytest.raises(
        ValueError,
        match="evaluated_at must be timezone-aware",
    ):
        create_context(
            evaluated_at=datetime(2026, 3, 15),
        )


def test_context_is_immutable() -> None:
    context = create_context()

    with pytest.raises(FrozenInstanceError):
        context.customer_id = "OTHER"


def test_exact_scope_matches_context() -> None:
    evaluation = evaluate()

    assert evaluation.match_status is (
        KnowledgeScopeMatchStatus.MATCHES
    )
    assert evaluation.mismatch_reasons == ()


@pytest.mark.parametrize(
    ("scope_overrides", "reason"),
    (
        (
            {"organization_id": "OTHER-ORG"},
            KnowledgeScopeMismatchReason.ORGANIZATION_MISMATCH,
        ),
        (
            {"customer_id": "OTHER-CUSTOMER"},
            KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH,
        ),
        (
            {"jurisdiction": "US"},
            KnowledgeScopeMismatchReason.JURISDICTION_MISMATCH,
        ),
        (
            {"commercial_channel_id": "ECOMMERCE"},
            (
                KnowledgeScopeMismatchReason
                .COMMERCIAL_CHANNEL_MISMATCH
            ),
        ),
        (
            {"document_type": KnowledgeDocumentType.LOOKBOOK},
            KnowledgeScopeMismatchReason.DOCUMENT_TYPE_MISMATCH,
        ),
        (
            {"point_of_sale_scope": explicit("POS-999")},
            KnowledgeScopeMismatchReason.POINT_OF_SALE_MISMATCH,
        ),
        (
            {"department_scope": explicit("DPT-FOOTWEAR")},
            KnowledgeScopeMismatchReason.DEPARTMENT_MISMATCH,
        ),
        (
            {"campaign_id": "CAMP-FALL-2026"},
            KnowledgeScopeMismatchReason.CAMPAIGN_MISMATCH,
        ),
    ),
)
def test_each_scope_mismatch_is_reported_explicitly(
    scope_overrides: dict[str, object],
    reason: KnowledgeScopeMismatchReason,
) -> None:
    evaluation = evaluate(
        scope=create_scope(**scope_overrides),
    )

    assert evaluation.match_status is (
        KnowledgeScopeMatchStatus.DOES_NOT_MATCH
    )
    assert evaluation.mismatch_reasons == (reason,)


def test_all_scope_matches_any_store_and_department() -> None:
    evaluation = evaluate(
        scope=create_scope(
            point_of_sale_scope=all_values(),
            department_scope=all_values(),
        ),
        context=create_context(
            point_of_sale_id="POS-999",
            department_id="DPT-FOOTWEAR",
        ),
    )

    assert evaluation.match_status is (
        KnowledgeScopeMatchStatus.MATCHES
    )


def test_multiple_mismatches_preserve_deterministic_order() -> None:
    evaluation = evaluate(
        scope=create_scope(
            organization_id="OTHER-ORG",
            customer_id="OTHER-CUSTOMER",
            point_of_sale_scope=explicit("POS-999"),
            campaign_id="OTHER-CAMPAIGN",
        ),
    )

    assert evaluation.mismatch_reasons == (
        KnowledgeScopeMismatchReason.ORGANIZATION_MISMATCH,
        KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH,
        KnowledgeScopeMismatchReason.POINT_OF_SALE_MISMATCH,
        KnowledgeScopeMismatchReason.CAMPAIGN_MISMATCH,
    )


def test_undeclared_campaign_matches_only_undeclared_context() -> None:
    matching = evaluate(
        scope=create_scope(campaign_id=None),
        context=create_context(campaign_id=None),
    )
    mismatching = evaluate(
        scope=create_scope(campaign_id=None),
        context=create_context(
            campaign_id="CAMP-SPRING-2026",
        ),
    )

    assert matching.match_status is (
        KnowledgeScopeMatchStatus.MATCHES
    )
    assert mismatching.mismatch_reasons == (
        KnowledgeScopeMismatchReason.CAMPAIGN_MISMATCH,
    )


def test_evaluation_rejects_untyped_inputs() -> None:
    with pytest.raises(
        TypeError,
        match="source_scope must be a KnowledgeSourceScope",
    ):
        evaluate_knowledge_source_scope(
            source_scope="scope",
            retrieval_context=create_context(),
        )

    with pytest.raises(
        TypeError,
        match="retrieval_context must be a",
    ):
        evaluate_knowledge_source_scope(
            source_scope=create_scope(),
            retrieval_context="context",
        )


def test_evaluation_contract_rejects_inconsistent_match() -> None:
    with pytest.raises(
        ValueError,
        match="MATCHES evaluation cannot contain",
    ):
        KnowledgeSourceScopeEvaluation(
            source_scope=create_scope(),
            retrieval_context=create_context(),
            match_status=KnowledgeScopeMatchStatus.MATCHES,
            mismatch_reasons=(
                KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH,
            ),
        )


def test_evaluation_contract_rejects_reasonless_mismatch() -> None:
    with pytest.raises(
        ValueError,
        match="DOES_NOT_MATCH evaluation requires",
    ):
        KnowledgeSourceScopeEvaluation(
            source_scope=create_scope(),
            retrieval_context=create_context(),
            match_status=(
                KnowledgeScopeMatchStatus.DOES_NOT_MATCH
            ),
            mismatch_reasons=(),
        )


def test_evaluation_is_immutable() -> None:
    evaluation = evaluate()

    with pytest.raises(FrozenInstanceError):
        evaluation.match_status = (
            KnowledgeScopeMatchStatus.DOES_NOT_MATCH
        )


def test_scope_evaluation_does_not_claim_retrieval_or_authority() -> None:
    evaluation = evaluate()

    for attribute in (
        "retrieval_decision",
        "included",
        "eligible",
        "valid",
        "authority_verified",
        "authentic",
        "relevant",
        "truth",
    ):
        assert not hasattr(evaluation, attribute)


def test_evaluation_preserves_inputs_without_mutation() -> None:
    scope = create_scope()
    context = create_context()

    scope_before = replace(scope)
    context_before = replace(context)

    evaluation = evaluate(
        scope=scope,
        context=context,
    )

    assert evaluation.source_scope is scope
    assert evaluation.retrieval_context is context
    assert scope == scope_before
    assert context == context_before
