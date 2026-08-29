from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityAdjudicationStatus,
    KnowledgeAuthorityBinding,
    KnowledgeAuthorityRelationshipType,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
    KnowledgeScopeMismatchReason,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeRetrievalExclusionReason,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeEvidenceStatus,
    KnowledgeLifecycleStatus,
    KnowledgeSourceStatus,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersession,
    KnowledgeSourceSupersessionGraph,
)
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)
from sp001.services.knowledge_source_retrieval import (
    evaluate_knowledge_source_retrieval,
)


CONTENT = b"approved denim planogram"
NOW = datetime(2026, 3, 15, 12, tzinfo=timezone.utc)


def selection(*ids: str) -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.EXPLICIT,
        ids=tuple(ids),
    )


def create_status(
    *,
    source_id: str = "POG-2026-DENIM-012",
    source_version: str = "current",
    lifecycle: KnowledgeLifecycleStatus = (
        KnowledgeLifecycleStatus.APPROVED
    ),
    evidence: KnowledgeEvidenceStatus = (
        KnowledgeEvidenceStatus.SUPPORTED
    ),
) -> KnowledgeSourceStatus:
    return KnowledgeSourceStatus(
        status_record_id=f"STATUS-{source_id}",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version=source_version,
            source_content_digest=(
                digest_knowledge_source_content(
                    content=CONTENT,
                )
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="RETAIL-GROUP-GLOBAL",
            customer_id="BRAND-CASUAL-X",
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL-STORE",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=selection("POS-045"),
            department_scope=selection("DPT-DENIM"),
            campaign_id="CAMP-SPRING-2026",
        ),
        lifecycle_status=lifecycle,
        evidence_status=evidence,
    )


def create_context(
    **overrides: object,
) -> KnowledgeRetrievalContext:
    values: dict[str, object] = {
        "organization_id": "RETAIL-GROUP-GLOBAL",
        "customer_id": "BRAND-CASUAL-X",
        "jurisdiction": "MX",
        "commercial_channel_id": "PHYSICAL-STORE",
        "document_type": KnowledgeDocumentType.PLANOGRAM,
        "point_of_sale_id": "POS-045",
        "department_id": "DPT-DENIM",
        "campaign_id": "CAMP-SPRING-2026",
        "evaluated_at": NOW,
    }
    values.update(overrides)
    return KnowledgeRetrievalContext(**values)


def create_actor() -> RetailProcessActor:
    return RetailProcessActor(
        actor_id="ACTOR-VM-DIRECTOR",
        customer_id="BRAND-CASUAL-X",
        actor_type=ActorType.HUMAN,
        organization_id="RETAIL-GROUP-GLOBAL",
        role=RetailProcessRole(
            role_id="ROLE-VM-DIRECTOR",
            customer_id="BRAND-CASUAL-X",
            role_name="VM_DIRECTOR",
        ),
    )


def create_binding(
    source: KnowledgeSourceStatus,
    *,
    adjudication: KnowledgeAuthorityAdjudicationStatus = (
        KnowledgeAuthorityAdjudicationStatus.VERIFIED
    ),
) -> KnowledgeAuthorityBinding:
    authority = create_status(
        source_id="DIR-VM-GLOBAL-2026",
        source_version="directive",
    )

    verified = (
        adjudication
        is KnowledgeAuthorityAdjudicationStatus.VERIFIED
    )

    return KnowledgeAuthorityBinding(
        authority_binding_id="AUTHORITY-BINDING-001",
        binding_version=1,
        governed_source_status=source,
        authority_source_status=authority,
        relationship_type=(
            KnowledgeAuthorityRelationshipType.GOVERNS
        ),
        adjudication_status=adjudication,
        adjudication_evidence_ids=(
            ("AUTHORITY-EVIDENCE-001",)
            if verified
            else ()
        ),
        adjudicated_by=create_actor() if verified else None,
        adjudicated_at=NOW if verified else None,
    )


def evaluate(
    *,
    source: KnowledgeSourceStatus | None = None,
    content: bytes = CONTENT,
    context: KnowledgeRetrievalContext | None = None,
    bindings: tuple[KnowledgeAuthorityBinding, ...] | None = None,
    graph: KnowledgeSourceSupersessionGraph | None = None,
    effective_from: datetime | None = None,
):
    selected_source = source or create_status()

    return evaluate_knowledge_source_retrieval(
        source_status=selected_source,
        content=content,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=selected_source,
            effective_from=effective_from or datetime(
                2026,
                3,
                1,
                tzinfo=timezone.utc,
            ),
        ),
        retrieval_context=context or create_context(),
        authority_bindings=(
            bindings
            if bindings is not None
            else (create_binding(selected_source),)
        ),
        supersession_graph=(
            graph
            if graph is not None
            else KnowledgeSourceSupersessionGraph(
                supersessions=(),
            )
        ),
    )


def test_decision_status_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeRetrievalDecisionStatus) == (
        KnowledgeRetrievalDecisionStatus.INCLUDED,
        KnowledgeRetrievalDecisionStatus.EXCLUDED,
    )


def test_exclusion_reason_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeRetrievalExclusionReason) == (
        KnowledgeRetrievalExclusionReason.CONTENT_BYTES_MISMATCH,
        KnowledgeRetrievalExclusionReason.SCOPE_MISMATCH,
        KnowledgeRetrievalExclusionReason.LIFECYCLE_NOT_APPROVED,
        KnowledgeRetrievalExclusionReason.EVIDENCE_NOT_SUPPORTED,
        KnowledgeRetrievalExclusionReason.TEMPORALLY_INACTIVE,
        (
            KnowledgeRetrievalExclusionReason
            .NO_VERIFIED_AUTHORITY_BINDING
        ),
        KnowledgeRetrievalExclusionReason.SOURCE_SUPERSEDED,
    )


def test_fully_supported_source_is_included() -> None:
    decision = evaluate()

    assert decision.decision_status is (
        KnowledgeRetrievalDecisionStatus.INCLUDED
    )
    assert decision.exclusion_reasons == ()
    assert decision.content_bytes_match_digest is True
    assert decision.verified_authority_binding_ids == (
        "AUTHORITY-BINDING-001",
    )


@pytest.mark.parametrize(
    ("mutation", "reason"),
    (
        (
            "content",
            KnowledgeRetrievalExclusionReason.CONTENT_BYTES_MISMATCH,
        ),
        (
            "scope",
            KnowledgeRetrievalExclusionReason.SCOPE_MISMATCH,
        ),
        (
            "lifecycle",
            (
                KnowledgeRetrievalExclusionReason
                .LIFECYCLE_NOT_APPROVED
            ),
        ),
        (
            "evidence",
            (
                KnowledgeRetrievalExclusionReason
                .EVIDENCE_NOT_SUPPORTED
            ),
        ),
        (
            "temporal",
            KnowledgeRetrievalExclusionReason.TEMPORALLY_INACTIVE,
        ),
        (
            "authority",
            (
                KnowledgeRetrievalExclusionReason
                .NO_VERIFIED_AUTHORITY_BINDING
            ),
        ),
    ),
)
def test_each_failed_control_excludes_source(
    mutation: str,
    reason: KnowledgeRetrievalExclusionReason,
) -> None:
    source = create_status(
        lifecycle=(
            KnowledgeLifecycleStatus.DRAFT
            if mutation == "lifecycle"
            else KnowledgeLifecycleStatus.APPROVED
        ),
        evidence=(
            KnowledgeEvidenceStatus.DISPUTED
            if mutation == "evidence"
            else KnowledgeEvidenceStatus.SUPPORTED
        ),
    )

    decision = evaluate(
        source=source,
        content=(
            b"modified"
            if mutation == "content"
            else CONTENT
        ),
        context=(
            create_context(customer_id="OTHER")
            if mutation == "scope"
            else create_context()
        ),
        bindings=(
            ()
            if mutation == "authority"
            else (create_binding(source),)
        ),
        effective_from=(
            datetime(2026, 4, 1, tzinfo=timezone.utc)
            if mutation == "temporal"
            else None
        ),
    )

    assert decision.decision_status is (
        KnowledgeRetrievalDecisionStatus.EXCLUDED
    )
    assert reason in decision.exclusion_reasons


def test_scope_details_are_preserved() -> None:
    decision = evaluate(
        context=create_context(customer_id="OTHER"),
    )

    assert decision.scope_evaluation.mismatch_reasons == (
        KnowledgeScopeMismatchReason.CUSTOMER_MISMATCH,
    )


def test_temporal_details_are_preserved() -> None:
    decision = evaluate(
        effective_from=datetime(
            2026,
            4,
            1,
            tzinfo=timezone.utc,
        ),
    )

    assert decision.temporal_evaluation.temporal_status is (
        KnowledgeTemporalApplicabilityStatus
        .NOT_YET_EFFECTIVE
    )


def test_superseded_predecessor_is_excluded() -> None:
    predecessor = create_status()
    successor = create_status(
        source_id="POG-2026-DENIM-013",
        source_version="successor",
    )
    supersession = KnowledgeSourceSupersession(
        supersession_id="SUPERSESSION-001",
        supersession_version=1,
        predecessor_source_status=predecessor,
        successor_source_status=successor,
        declaration_evidence_ids=("SUPERSESSION-EVIDENCE-001",),
        declared_by=create_actor(),
        declared_at=NOW,
    )

    decision = evaluate(
        source=predecessor,
        graph=KnowledgeSourceSupersessionGraph(
            supersessions=(supersession,),
        ),
    )

    assert decision.supersession_ids == ("SUPERSESSION-001",)
    assert decision.exclusion_reasons == (
        KnowledgeRetrievalExclusionReason.SOURCE_SUPERSEDED,
    )


def test_successor_is_not_automatically_included() -> None:
    predecessor = create_status(
        source_id="POG-OLD",
        source_version="old",
    )
    successor = create_status(
        source_id="POG-NEW",
        source_version="new",
        evidence=KnowledgeEvidenceStatus.DISPUTED,
    )
    graph = KnowledgeSourceSupersessionGraph(
        supersessions=(
            KnowledgeSourceSupersession(
                supersession_id="SUPERSESSION-001",
                supersession_version=1,
                predecessor_source_status=predecessor,
                successor_source_status=successor,
                declaration_evidence_ids=("EVIDENCE-001",),
                declared_by=create_actor(),
                declared_at=NOW,
            ),
        ),
    )

    decision = evaluate(
        source=successor,
        graph=graph,
    )

    assert decision.decision_status is (
        KnowledgeRetrievalDecisionStatus.EXCLUDED
    )
    assert decision.supersession_ids == ()
    assert decision.exclusion_reasons == (
        KnowledgeRetrievalExclusionReason.EVIDENCE_NOT_SUPPORTED,
    )


def test_multiple_failures_preserve_deterministic_order() -> None:
    source = create_status(
        lifecycle=KnowledgeLifecycleStatus.DRAFT,
        evidence=KnowledgeEvidenceStatus.DISPUTED,
    )

    decision = evaluate(
        source=source,
        content=b"modified",
        context=create_context(customer_id="OTHER"),
        bindings=(),
        effective_from=datetime(
            2026,
            4,
            1,
            tzinfo=timezone.utc,
        ),
    )

    assert decision.exclusion_reasons == (
        KnowledgeRetrievalExclusionReason.CONTENT_BYTES_MISMATCH,
        KnowledgeRetrievalExclusionReason.SCOPE_MISMATCH,
        KnowledgeRetrievalExclusionReason.LIFECYCLE_NOT_APPROVED,
        KnowledgeRetrievalExclusionReason.EVIDENCE_NOT_SUPPORTED,
        KnowledgeRetrievalExclusionReason.TEMPORALLY_INACTIVE,
        (
            KnowledgeRetrievalExclusionReason
            .NO_VERIFIED_AUTHORITY_BINDING
        ),
    )


def test_unverified_binding_does_not_satisfy_control() -> None:
    source = create_status()

    decision = evaluate(
        source=source,
        bindings=(
            create_binding(
                source,
                adjudication=(
                    KnowledgeAuthorityAdjudicationStatus.UNVERIFIED
                ),
            ),
        ),
    )

    assert decision.verified_authority_binding_ids == ()
    assert decision.exclusion_reasons == (
        KnowledgeRetrievalExclusionReason
        .NO_VERIFIED_AUTHORITY_BINDING,
    )


def test_period_must_describe_exact_source_status() -> None:
    source = create_status()
    other = create_status(source_id="OTHER")

    with pytest.raises(
        ValueError,
        match="effective_period must describe source_status",
    ):
        evaluate_knowledge_source_retrieval(
            source_status=source,
            content=CONTENT,
            effective_period=KnowledgeSourceEffectivePeriod(
                source_status=other,
                effective_from=NOW,
            ),
            retrieval_context=create_context(),
            authority_bindings=(create_binding(source),),
            supersession_graph=KnowledgeSourceSupersessionGraph(
                supersessions=(),
            ),
        )


def test_decision_is_immutable() -> None:
    decision = evaluate()

    with pytest.raises(FrozenInstanceError):
        decision.decision_status = (
            KnowledgeRetrievalDecisionStatus.EXCLUDED
        )


def test_decision_preserves_inputs_without_mutation() -> None:
    source = create_status()
    source_before = replace(source)

    decision = evaluate(source=source)

    assert decision.source_status is source
    assert source == source_before


def test_decision_does_not_claim_truth_relevance_or_legal_authority() -> None:
    decision = evaluate()

    for attribute in (
        "valid",
        "truth",
        "correct",
        "authentic",
        "semantically_relevant",
        "legally_authoritative",
        "recommendation",
        "compliance_status",
    ):
        assert not hasattr(decision, attribute)
