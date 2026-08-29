from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityAdjudicationStatus,
    KnowledgeAuthorityBinding,
    KnowledgeAuthorityRelationshipType,
)
from sp001.contracts.knowledge_retrieval_candidate import (
    KnowledgeRetrievalCandidate,
    KnowledgeRetrievalCandidateSet,
)
from sp001.contracts.knowledge_retrieval_context import (
    KnowledgeRetrievalContext,
)
from sp001.contracts.knowledge_retrieval_decision import (
    KnowledgeRetrievalDecisionStatus,
    KnowledgeRetrievalExclusionReason,
)
from sp001.contracts.knowledge_retrieval_manifest import (
    KnowledgeRetrievalCandidateDecision,
    KnowledgeRetrievalManifest,
)
from sp001.contracts.knowledge_source_effective_period import (
    KnowledgeSourceEffectivePeriod,
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
    KnowledgeSourceSupersessionGraph,
)
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)
from sp001.services.knowledge_retrieval_manifest import (
    evaluate_knowledge_retrieval_candidates,
)
from sp001.services.knowledge_source_integrity import (
    digest_knowledge_source_content,
)


CONTENT = b"governed planogram"
NOW = datetime(2026, 3, 15, 12, tzinfo=timezone.utc)


def selection(identity: str) -> KnowledgeScopeSelection:
    return KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.EXPLICIT,
        ids=(identity,),
    )


def create_status(
    *,
    source_id: str,
    evidence: KnowledgeEvidenceStatus = (
        KnowledgeEvidenceStatus.SUPPORTED
    ),
) -> KnowledgeSourceStatus:
    return KnowledgeSourceStatus(
        status_record_id=f"STATUS-{source_id}",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version="v1",
            source_content_digest=(
                digest_knowledge_source_content(
                    content=CONTENT,
                )
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="ORG-001",
            customer_id="CUSTOMER-001",
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL-STORE",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=selection("POS-045"),
            department_scope=selection("DPT-DENIM"),
            campaign_id="CAMP-001",
        ),
        lifecycle_status=KnowledgeLifecycleStatus.APPROVED,
        evidence_status=evidence,
    )


def create_context(
    *,
    customer_id: str = "CUSTOMER-001",
) -> KnowledgeRetrievalContext:
    return KnowledgeRetrievalContext(
        organization_id="ORG-001",
        customer_id=customer_id,
        jurisdiction="MX",
        commercial_channel_id="PHYSICAL-STORE",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_id="POS-045",
        department_id="DPT-DENIM",
        campaign_id="CAMP-001",
        evaluated_at=NOW,
    )


def create_actor() -> RetailProcessActor:
    return RetailProcessActor(
        actor_id="ACTOR-001",
        customer_id="CUSTOMER-001",
        actor_type=ActorType.HUMAN,
        organization_id="ORG-001",
        role=RetailProcessRole(
            role_id="ROLE-001",
            customer_id="CUSTOMER-001",
            role_name="VM_DIRECTOR",
        ),
    )


def create_binding(
    source: KnowledgeSourceStatus,
) -> KnowledgeAuthorityBinding:
    authority = create_status(
        source_id="AUTHORITY-SOURCE",
    )

    return KnowledgeAuthorityBinding(
        authority_binding_id=f"BINDING-{source.identity.source_id}",
        binding_version=1,
        governed_source_status=source,
        authority_source_status=authority,
        relationship_type=(
            KnowledgeAuthorityRelationshipType.GOVERNS
        ),
        adjudication_status=(
            KnowledgeAuthorityAdjudicationStatus.VERIFIED
        ),
        adjudication_evidence_ids=("EVIDENCE-001",),
        adjudicated_by=create_actor(),
        adjudicated_at=NOW,
    )


def create_candidate(
    *,
    candidate_id: str,
    source_id: str,
    included: bool,
) -> KnowledgeRetrievalCandidate:
    source = create_status(
        source_id=source_id,
        evidence=(
            KnowledgeEvidenceStatus.SUPPORTED
            if included
            else KnowledgeEvidenceStatus.DISPUTED
        ),
    )

    return KnowledgeRetrievalCandidate(
        candidate_id=candidate_id,
        source_status=source,
        content=CONTENT,
        effective_period=KnowledgeSourceEffectivePeriod(
            source_status=source,
            effective_from=datetime(
                2026,
                3,
                1,
                tzinfo=timezone.utc,
            ),
        ),
        authority_bindings=(create_binding(source),),
    )


def create_candidate_set(
    *candidates: KnowledgeRetrievalCandidate,
    context: KnowledgeRetrievalContext | None = None,
) -> KnowledgeRetrievalCandidateSet:
    return KnowledgeRetrievalCandidateSet(
        retrieval_context=context or create_context(),
        candidates=tuple(candidates),
        supersession_graph=KnowledgeSourceSupersessionGraph(
            supersessions=(),
        ),
    )


def create_manifest() -> KnowledgeRetrievalManifest:
    return evaluate_knowledge_retrieval_candidates(
        candidate_set=create_candidate_set(
            create_candidate(
                candidate_id="CANDIDATE-001",
                source_id="SOURCE-001",
                included=True,
            ),
            create_candidate(
                candidate_id="CANDIDATE-002",
                source_id="SOURCE-002",
                included=False,
            ),
            create_candidate(
                candidate_id="CANDIDATE-003",
                source_id="SOURCE-003",
                included=True,
            ),
        ),
    )


def test_empty_candidate_set_produces_empty_manifest() -> None:
    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=create_candidate_set(),
    )

    assert manifest.candidate_decisions == ()
    assert manifest.all_decisions == ()
    assert manifest.included_decisions == ()
    assert manifest.excluded_decisions == ()


def test_manifest_preserves_candidate_order_and_identity() -> None:
    manifest = create_manifest()

    assert tuple(
        record.candidate_id
        for record in manifest.candidate_decisions
    ) == (
        "CANDIDATE-001",
        "CANDIDATE-002",
        "CANDIDATE-003",
    )


def test_all_decisions_preserve_complete_universe() -> None:
    manifest = create_manifest()

    assert len(manifest.all_decisions) == 3
    assert tuple(
        decision.source_status.identity.source_id
        for decision in manifest.all_decisions
    ) == (
        "SOURCE-001",
        "SOURCE-002",
        "SOURCE-003",
    )


def test_included_view_preserves_relative_order() -> None:
    manifest = create_manifest()

    assert tuple(
        decision.source_status.identity.source_id
        for decision in manifest.included_decisions
    ) == (
        "SOURCE-001",
        "SOURCE-003",
    )


def test_excluded_view_preserves_relative_order_and_reasons() -> None:
    manifest = create_manifest()

    assert tuple(
        decision.source_status.identity.source_id
        for decision in manifest.excluded_decisions
    ) == ("SOURCE-002",)

    assert manifest.excluded_decisions[0].exclusion_reasons == (
        KnowledgeRetrievalExclusionReason
        .EVIDENCE_NOT_SUPPORTED,
    )


def test_views_form_lossless_disjoint_partition() -> None:
    manifest = create_manifest()

    included = set(manifest.included_decisions)
    excluded = set(manifest.excluded_decisions)

    assert included.isdisjoint(excluded)
    assert included | excluded == set(
        manifest.all_decisions
    )


def test_every_candidate_is_evaluated_exactly_once() -> None:
    manifest = create_manifest()

    assert len(manifest.candidate_decisions) == 3
    assert len({
        record.candidate_id
        for record in manifest.candidate_decisions
    }) == 3


def test_manifest_uses_candidate_set_context() -> None:
    context = create_context()
    candidate_set = create_candidate_set(
        create_candidate(
            candidate_id="CANDIDATE-001",
            source_id="SOURCE-001",
            included=True,
        ),
        context=context,
    )

    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=candidate_set,
    )

    assert manifest.retrieval_context is context
    assert (
        manifest.all_decisions[0].retrieval_context
        is context
    )


def test_context_mismatch_excludes_every_affected_candidate() -> None:
    manifest = evaluate_knowledge_retrieval_candidates(
        candidate_set=create_candidate_set(
            create_candidate(
                candidate_id="CANDIDATE-001",
                source_id="SOURCE-001",
                included=True,
            ),
            context=create_context(customer_id="OTHER"),
        ),
    )

    assert manifest.all_decisions[0].decision_status is (
        KnowledgeRetrievalDecisionStatus.EXCLUDED
    )
    assert manifest.all_decisions[0].exclusion_reasons == (
        KnowledgeRetrievalExclusionReason.SCOPE_MISMATCH,
    )


def test_manifest_rejects_mutable_record_collection() -> None:
    with pytest.raises(
        TypeError,
        match="candidate_decisions must be an immutable tuple",
    ):
        KnowledgeRetrievalManifest(
            retrieval_context=create_context(),
            candidate_decisions=[],
        )


def test_manifest_rejects_untyped_records() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeRetrievalCandidateDecision values",
    ):
        KnowledgeRetrievalManifest(
            retrieval_context=create_context(),
            candidate_decisions=("record",),
        )


def test_manifest_rejects_duplicate_candidate_identity() -> None:
    manifest = create_manifest()
    record = manifest.candidate_decisions[0]

    with pytest.raises(
        ValueError,
        match="duplicate candidate_id",
    ):
        KnowledgeRetrievalManifest(
            retrieval_context=manifest.retrieval_context,
            candidate_decisions=(record, record),
        )


def test_manifest_is_immutable() -> None:
    manifest = create_manifest()

    with pytest.raises(FrozenInstanceError):
        manifest.candidate_decisions = ()


def test_evaluator_rejects_untyped_candidate_set() -> None:
    with pytest.raises(
        TypeError,
        match="KnowledgeRetrievalCandidateSet",
    ):
        evaluate_knowledge_retrieval_candidates(
            candidate_set="candidate-set",
        )


def test_manifest_does_not_claim_ranking_or_semantic_relevance() -> None:
    manifest = create_manifest()

    for attribute in (
        "ranking",
        "scores",
        "top_k",
        "semantic_relevance",
        "recommended_sources",
        "answer",
        "embedding",
    ):
        assert not hasattr(manifest, attribute)
