from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeSourceScopeEvaluation,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeSourceRetrievalDecision,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
    KnowledgeRetrievalManifest,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
    KnowledgeSourceTemporalEvaluation,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
    KnowledgeSourceIdentity,
)
from sp001.contracts.knowledge_source_scope import (
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.knowledge_source_status import (
    KnowledgeSourceStatus,
)
from sp001.services.knowledge_governed_retrieval_query_context_projection import (
    project_knowledge_retrieval_context,
)


def project_knowledge_retrieval_manifest(
    *,
    manifest: KnowledgeRetrievalManifest,
) -> dict[str, object]:
    """Project every declared governance disposition without inference."""

    if not isinstance(
        manifest,
        KnowledgeRetrievalManifest,
    ):
        raise TypeError(
            "manifest must be a KnowledgeRetrievalManifest"
        )

    return {
        "retrieval_context": project_knowledge_retrieval_context(
            context=manifest.retrieval_context,
        ),
        "candidate_decisions": [
            _candidate_decision_document(candidate)
            for candidate in manifest.candidate_decisions
        ],
    }


def _candidate_decision_document(
    candidate: KnowledgeRetrievalCandidateDecision,
) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "decision": _retrieval_decision_document(
            candidate.decision
        ),
    }


def _retrieval_decision_document(
    decision: KnowledgeSourceRetrievalDecision,
) -> dict[str, object]:
    return {
        "source_status": _source_status_document(
            decision.source_status
        ),
        "retrieval_context": project_knowledge_retrieval_context(
            context=decision.retrieval_context,
        ),
        "content_bytes_match_digest": (
            decision.content_bytes_match_digest
        ),
        "scope_evaluation": _scope_evaluation_document(
            decision.scope_evaluation
        ),
        "temporal_evaluation": _temporal_evaluation_document(
            decision.temporal_evaluation
        ),
        "verified_authority_binding_ids": list(
            decision.verified_authority_binding_ids
        ),
        "supersession_ids": list(
            decision.supersession_ids
        ),
        "decision_status": decision.decision_status.value,
        "exclusion_reasons": [
            reason.value
            for reason in decision.exclusion_reasons
        ],
    }


def _source_status_document(
    status: KnowledgeSourceStatus,
) -> dict[str, object]:
    return {
        "status_record_id": status.status_record_id,
        "status_version": status.status_version,
        "identity": _source_identity_document(
            status.identity
        ),
        "scope": _source_scope_document(
            status.scope
        ),
        "lifecycle_status": status.lifecycle_status.value,
        "evidence_status": status.evidence_status.value,
    }


def _source_identity_document(
    identity: KnowledgeSourceIdentity,
) -> dict[str, object]:
    return {
        "source_id": identity.source_id,
        "source_version": identity.source_version,
        "source_content_digest": _content_digest_document(
            identity.source_content_digest
        ),
    }


def _content_digest_document(
    digest: KnowledgeContentDigest,
) -> dict[str, object]:
    return {
        "algorithm": digest.algorithm,
        "value": digest.value,
    }


def _source_scope_document(
    scope: KnowledgeSourceScope,
) -> dict[str, object]:
    return {
        "organization_id": scope.organization_id,
        "customer_id": scope.customer_id,
        "jurisdiction": scope.jurisdiction,
        "commercial_channel_id": (
            scope.commercial_channel_id
        ),
        "document_type": scope.document_type.value,
        "point_of_sale_scope": _scope_selection_document(
            scope.point_of_sale_scope
        ),
        "department_scope": _scope_selection_document(
            scope.department_scope
        ),
        "campaign_id": scope.campaign_id,
    }


def _scope_selection_document(
    selection: KnowledgeScopeSelection,
) -> dict[str, object]:
    return {
        "mode": selection.mode.value,
        "ids": list(selection.ids),
    }


def _scope_evaluation_document(
    evaluation: KnowledgeSourceScopeEvaluation,
) -> dict[str, object]:
    return {
        "source_scope": _source_scope_document(
            evaluation.source_scope
        ),
        "retrieval_context": project_knowledge_retrieval_context(
            context=evaluation.retrieval_context,
        ),
        "match_status": evaluation.match_status.value,
        "mismatch_reasons": [
            reason.value
            for reason in evaluation.mismatch_reasons
        ],
    }


def _temporal_evaluation_document(
    evaluation: KnowledgeSourceTemporalEvaluation,
) -> dict[str, object]:
    return {
        "effective_period": _effective_period_document(
            evaluation.effective_period
        ),
        "evaluated_at": evaluation.evaluated_at.isoformat(),
        "temporal_status": evaluation.temporal_status.value,
    }


def _effective_period_document(
    period: KnowledgeSourceEffectivePeriod,
) -> dict[str, object]:
    return {
        "source_status": _source_status_document(
            period.source_status
        ),
        "effective_from": period.effective_from.isoformat(),
        "effective_until": (
            period.effective_until.isoformat()
            if period.effective_until is not None
            else None
        ),
    }
