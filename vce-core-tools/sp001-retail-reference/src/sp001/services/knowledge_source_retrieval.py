from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityAdjudicationStatus,
    KnowledgeAuthorityBinding,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
    KnowledgeScopeMatchStatus,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeRetrievalExclusionReason,
    KnowledgeSourceRetrievalDecision,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
    KnowledgeTemporalApplicabilityStatus,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeEvidenceStatus,
    KnowledgeLifecycleStatus,
    KnowledgeSourceStatus,
)
from sp001.contracts.knowledge_source_supersession import (
    KnowledgeSourceSupersessionGraph,
)
from sp001.services.knowledge_source_integrity import (
    verify_knowledge_source_content,
)
from sp001.services.knowledge_source_scope_matching import (
    evaluate_knowledge_source_scope,
)
from sp001.services.knowledge_source_temporal_applicability import (
    evaluate_knowledge_source_temporal_applicability,
)


def evaluate_knowledge_source_retrieval(
    *,
    source_status: KnowledgeSourceStatus,
    content: bytes,
    effective_period: KnowledgeSourceEffectivePeriod,
    retrieval_context: KnowledgeRetrievalContext,
    authority_bindings: tuple[
        KnowledgeAuthorityBinding,
        ...,
    ],
    supersession_graph: KnowledgeSourceSupersessionGraph,
) -> KnowledgeSourceRetrievalDecision:
    """Compose declared controls into one auditable decision."""

    if not isinstance(source_status, KnowledgeSourceStatus):
        raise TypeError(
            "source_status must be a KnowledgeSourceStatus"
        )

    if not isinstance(
        effective_period,
        KnowledgeSourceEffectivePeriod,
    ):
        raise TypeError(
            "effective_period must be a "
            "KnowledgeSourceEffectivePeriod"
        )

    if effective_period.source_status != source_status:
        raise ValueError(
            "effective_period must describe source_status"
        )

    if not isinstance(
        retrieval_context,
        KnowledgeRetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a "
            "KnowledgeRetrievalContext"
        )

    if not isinstance(authority_bindings, tuple):
        raise TypeError(
            "authority_bindings must be an immutable tuple"
        )

    for binding in authority_bindings:
        if not isinstance(binding, KnowledgeAuthorityBinding):
            raise TypeError(
                "authority_bindings must contain "
                "KnowledgeAuthorityBinding values"
            )

    if not isinstance(
        supersession_graph,
        KnowledgeSourceSupersessionGraph,
    ):
        raise TypeError(
            "supersession_graph must be a "
            "KnowledgeSourceSupersessionGraph"
        )

    content_matches = verify_knowledge_source_content(
        identity=source_status.identity,
        content=content,
    )

    scope_evaluation = evaluate_knowledge_source_scope(
        source_scope=source_status.scope,
        retrieval_context=retrieval_context,
    )

    temporal_evaluation = (
        evaluate_knowledge_source_temporal_applicability(
            effective_period=effective_period,
            evaluated_at=retrieval_context.evaluated_at,
        )
    )

    verified_binding_ids = tuple(
        binding.authority_binding_id
        for binding in authority_bindings
        if (
            binding.governed_source_status == source_status
            and binding.adjudication_status
            is KnowledgeAuthorityAdjudicationStatus.VERIFIED
        )
    )

    supersession_ids = tuple(
        supersession.supersession_id
        for supersession in supersession_graph.supersessions
        if (
            supersession.predecessor_source_status.identity
            == source_status.identity
        )
    )

    reasons: list[
        KnowledgeRetrievalExclusionReason
    ] = []

    if not content_matches:
        reasons.append(
            KnowledgeRetrievalExclusionReason
            .CONTENT_BYTES_MISMATCH
        )

    if (
        scope_evaluation.match_status
        is KnowledgeScopeMatchStatus.DOES_NOT_MATCH
    ):
        reasons.append(
            KnowledgeRetrievalExclusionReason.SCOPE_MISMATCH
        )

    if (
        source_status.lifecycle_status
        is not KnowledgeLifecycleStatus.APPROVED
    ):
        reasons.append(
            KnowledgeRetrievalExclusionReason
            .LIFECYCLE_NOT_APPROVED
        )

    if (
        source_status.evidence_status
        is not KnowledgeEvidenceStatus.SUPPORTED
    ):
        reasons.append(
            KnowledgeRetrievalExclusionReason
            .EVIDENCE_NOT_SUPPORTED
        )

    if (
        temporal_evaluation.temporal_status
        is not KnowledgeTemporalApplicabilityStatus.ACTIVE
    ):
        reasons.append(
            KnowledgeRetrievalExclusionReason
            .TEMPORALLY_INACTIVE
        )

    if not verified_binding_ids:
        reasons.append(
            KnowledgeRetrievalExclusionReason
            .NO_VERIFIED_AUTHORITY_BINDING
        )

    if supersession_ids:
        reasons.append(
            KnowledgeRetrievalExclusionReason.SOURCE_SUPERSEDED
        )

    exclusion_reasons = tuple(reasons)

    decision_status = (
        KnowledgeRetrievalDecisionStatus.EXCLUDED
        if exclusion_reasons
        else KnowledgeRetrievalDecisionStatus.INCLUDED
    )

    return KnowledgeSourceRetrievalDecision(
        source_status=source_status,
        retrieval_context=retrieval_context,
        content_bytes_match_digest=content_matches,
        scope_evaluation=scope_evaluation,
        temporal_evaluation=temporal_evaluation,
        verified_authority_binding_ids=verified_binding_ids,
        supersession_ids=supersession_ids,
        decision_status=decision_status,
        exclusion_reasons=exclusion_reasons,
    )
