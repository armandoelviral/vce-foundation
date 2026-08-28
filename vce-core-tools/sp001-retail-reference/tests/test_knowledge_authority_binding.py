from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from sp001.contracts.knowledge_authority_binding import (
    KnowledgeAuthorityAdjudicationStatus,
    KnowledgeAuthorityBinding,
    KnowledgeAuthorityRelationshipType,
)
from sp001.contracts.knowledge_source_identity import (
    KnowledgeContentDigest,
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
from sp001.contracts.retail_process_actor import (
    ActorType,
    RetailProcessActor,
)
from sp001.contracts.retail_process_role import (
    RetailProcessRole,
)


ADJUDICATED_AT = datetime(
    2026,
    8,
    28,
    tzinfo=timezone.utc,
)


def create_source_status(
    *,
    source_id: str,
    document_type: KnowledgeDocumentType,
    customer_id: str = "BRAND-CASUAL-X",
) -> KnowledgeSourceStatus:
    digest_value = (
        "0" * 64
        if source_id.startswith("POG")
        else "1" * 64
    )

    return KnowledgeSourceStatus(
        status_record_id=f"STATUS-{source_id}",
        status_version=1,
        identity=KnowledgeSourceIdentity(
            source_id=source_id,
            source_version="v1.0",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value=digest_value,
            ),
        ),
        scope=KnowledgeSourceScope(
            organization_id="RETAIL-GROUP-GLOBAL",
            customer_id=customer_id,
            jurisdiction="MX",
            commercial_channel_id="PHYSICAL_STORE",
            document_type=document_type,
            point_of_sale_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.ALL,
                ids=(),
            ),
            department_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.ALL,
                ids=(),
            ),
        ),
        lifecycle_status=KnowledgeLifecycleStatus.APPROVED,
        evidence_status=KnowledgeEvidenceStatus.SUPPORTED,
    )


def governed_source() -> KnowledgeSourceStatus:
    return create_source_status(
        source_id="POG-2026-DENIM-012",
        document_type=KnowledgeDocumentType.PLANOGRAM,
    )


def authority_source() -> KnowledgeSourceStatus:
    return create_source_status(
        source_id="DIR-VM-GLOBAL-2026",
        document_type=KnowledgeDocumentType.VISUAL_MANUAL,
    )


def create_actor(
    *,
    customer_id: str = "BRAND-CASUAL-X",
    actor_type: ActorType = ActorType.HUMAN,
) -> RetailProcessActor:
    return RetailProcessActor(
        actor_id="ACTOR-VM-DIRECTOR",
        customer_id=customer_id,
        actor_type=actor_type,
        organization_id="RETAIL-GROUP-GLOBAL",
        role=RetailProcessRole(
            role_id="ROLE-VM-DIRECTOR",
            customer_id=customer_id,
            role_name="VM_DIRECTOR",
        ),
    )


def create_binding(
    **overrides: object,
) -> KnowledgeAuthorityBinding:
    values = {
        "authority_binding_id": "AUTHORITY-BINDING-001",
        "binding_version": 1,
        "governed_source_status": governed_source(),
        "authority_source_status": authority_source(),
        "relationship_type": (
            KnowledgeAuthorityRelationshipType.GOVERNS
        ),
        "adjudication_status": (
            KnowledgeAuthorityAdjudicationStatus.UNVERIFIED
        ),
        "adjudication_evidence_ids": (),
        "adjudicated_by": None,
        "adjudicated_at": None,
    }
    values.update(overrides)

    return KnowledgeAuthorityBinding(
        **values,
    )


def verified_binding() -> KnowledgeAuthorityBinding:
    return create_binding(
        adjudication_status=(
            KnowledgeAuthorityAdjudicationStatus.VERIFIED
        ),
        adjudication_evidence_ids=(
            "AUTHORITY-EVIDENCE-001",
        ),
        adjudicated_by=create_actor(),
        adjudicated_at=ADJUDICATED_AT,
    )


def test_relationship_vocabulary_is_exact() -> None:
    assert tuple(
        KnowledgeAuthorityRelationshipType
    ) == (
        KnowledgeAuthorityRelationshipType.GOVERNS,
        KnowledgeAuthorityRelationshipType.DELEGATES,
    )


def test_adjudication_vocabulary_is_exact() -> None:
    assert tuple(
        KnowledgeAuthorityAdjudicationStatus
    ) == (
        KnowledgeAuthorityAdjudicationStatus.UNVERIFIED,
        KnowledgeAuthorityAdjudicationStatus.VERIFIED,
        KnowledgeAuthorityAdjudicationStatus.REVOKED,
    )


def test_unverified_binding_preserves_reference_without_adjudication() -> None:
    binding = create_binding()

    assert binding.governed_source_status.identity.source_id == (
        "POG-2026-DENIM-012"
    )
    assert binding.authority_source_status.identity.source_id == (
        "DIR-VM-GLOBAL-2026"
    )
    assert binding.adjudication_status is (
        KnowledgeAuthorityAdjudicationStatus.UNVERIFIED
    )
    assert binding.adjudication_evidence_ids == ()
    assert binding.adjudicated_by is None
    assert binding.adjudicated_at is None


def test_verified_binding_requires_explicit_adjudication_record() -> None:
    binding = verified_binding()

    assert binding.adjudication_status is (
        KnowledgeAuthorityAdjudicationStatus.VERIFIED
    )
    assert binding.adjudication_evidence_ids == (
        "AUTHORITY-EVIDENCE-001",
    )
    assert binding.adjudicated_by.actor_id == (
        "ACTOR-VM-DIRECTOR"
    )
    assert binding.adjudicated_at == ADJUDICATED_AT


def test_revoked_binding_preserves_revocation_adjudication() -> None:
    binding = create_binding(
        adjudication_status=(
            KnowledgeAuthorityAdjudicationStatus.REVOKED
        ),
        adjudication_evidence_ids=(
            "REVOCATION-EVIDENCE-001",
        ),
        adjudicated_by=create_actor(),
        adjudicated_at=ADJUDICATED_AT,
    )

    assert binding.adjudication_status is (
        KnowledgeAuthorityAdjudicationStatus.REVOKED
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
def test_binding_rejects_empty_identity(
    invalid_id: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="authority_binding_id must not be empty",
    ):
        create_binding(
            authority_binding_id=invalid_id,
        )


@pytest.mark.parametrize(
    "invalid_version",
    (
        True,
        0,
        -1,
        1.0,
        "1",
    ),
)
def test_binding_rejects_invalid_version(
    invalid_version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "binding_version must be "
            "a positive integer"
        ),
    ):
        create_binding(
            binding_version=invalid_version,
        )


@pytest.mark.parametrize(
    "field",
    (
        "governed_source_status",
        "authority_source_status",
    ),
)
def test_binding_rejects_untyped_source_status(
    field: str,
) -> None:
    with pytest.raises(
        TypeError,
        match=f"{field} must be a KnowledgeSourceStatus",
    ):
        create_binding(
            **{
                field: "SOURCE-001",
            },
        )


def test_source_cannot_govern_itself() -> None:
    source = governed_source()

    with pytest.raises(
        ValueError,
        match="source cannot govern itself",
    ):
        create_binding(
            governed_source_status=source,
            authority_source_status=source,
        )


def test_binding_rejects_untyped_relationship() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "relationship_type must be a "
            "KnowledgeAuthorityRelationshipType"
        ),
    ):
        create_binding(
            relationship_type="GOVERNS",
        )


def test_binding_rejects_untyped_adjudication_status() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "adjudication_status must be a "
            "KnowledgeAuthorityAdjudicationStatus"
        ),
    ):
        create_binding(
            adjudication_status="VERIFIED",
        )


def test_binding_rejects_mutable_evidence_collection() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "adjudication_evidence_ids must be "
            "an immutable tuple"
        ),
    ):
        create_binding(
            adjudication_evidence_ids=[
                "AUTHORITY-EVIDENCE-001",
            ],
        )


def test_binding_rejects_duplicate_evidence_identity() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "duplicate adjudication evidence_id"
        ),
    ):
        create_binding(
            adjudication_evidence_ids=(
                "EVIDENCE-001",
                "EVIDENCE-001",
            ),
        )


def test_unverified_binding_rejects_adjudication_evidence() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "UNVERIFIED binding cannot contain "
            "adjudication evidence"
        ),
    ):
        create_binding(
            adjudication_evidence_ids=(
                "EVIDENCE-001",
            ),
        )


@pytest.mark.parametrize(
    "status",
    (
        KnowledgeAuthorityAdjudicationStatus.VERIFIED,
        KnowledgeAuthorityAdjudicationStatus.REVOKED,
    ),
)
def test_adjudicated_binding_requires_evidence(
    status: KnowledgeAuthorityAdjudicationStatus,
) -> None:
    with pytest.raises(
        ValueError,
        match="adjudicated binding requires evidence",
    ):
        create_binding(
            adjudication_status=status,
        )


def test_adjudicated_binding_requires_typed_actor() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "adjudicated_by must be a "
            "RetailProcessActor"
        ),
    ):
        create_binding(
            adjudication_status=(
                KnowledgeAuthorityAdjudicationStatus.VERIFIED
            ),
            adjudication_evidence_ids=(
                "EVIDENCE-001",
            ),
            adjudicated_by="ACTOR-001",
            adjudicated_at=ADJUDICATED_AT,
        )


def test_system_actor_cannot_adjudicate_authority() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "SYSTEM actor cannot adjudicate authority"
        ),
    ):
        create_binding(
            adjudication_status=(
                KnowledgeAuthorityAdjudicationStatus.VERIFIED
            ),
            adjudication_evidence_ids=(
                "EVIDENCE-001",
            ),
            adjudicated_by=create_actor(
                actor_type=ActorType.SYSTEM,
            ),
            adjudicated_at=ADJUDICATED_AT,
        )


def test_cross_customer_actor_cannot_adjudicate_binding() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "adjudicator customer must match "
            "governed source customer"
        ),
    ):
        create_binding(
            adjudication_status=(
                KnowledgeAuthorityAdjudicationStatus.VERIFIED
            ),
            adjudication_evidence_ids=(
                "EVIDENCE-001",
            ),
            adjudicated_by=create_actor(
                customer_id="CUSTOMER-B",
            ),
            adjudicated_at=ADJUDICATED_AT,
        )


def test_adjudicated_binding_requires_timezone_aware_time() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "adjudicated_at must be timezone-aware"
        ),
    ):
        create_binding(
            adjudication_status=(
                KnowledgeAuthorityAdjudicationStatus.VERIFIED
            ),
            adjudication_evidence_ids=(
                "EVIDENCE-001",
            ),
            adjudicated_by=create_actor(),
            adjudicated_at=datetime(
                2026,
                8,
                28,
            ),
        )


def test_binding_is_immutable() -> None:
    binding = verified_binding()

    with pytest.raises(FrozenInstanceError):
        binding.binding_version = 2


def test_verified_binding_does_not_mutate_source_statuses() -> None:
    binding = verified_binding()

    assert (
        binding.governed_source_status.lifecycle_status
        is KnowledgeLifecycleStatus.APPROVED
    )
    assert (
        binding.authority_source_status.lifecycle_status
        is KnowledgeLifecycleStatus.APPROVED
    )


def test_binding_does_not_claim_external_legal_authority() -> None:
    binding = verified_binding()

    for attribute in (
        "legally_authoritative",
        "signature_verified",
        "identity_authenticated",
        "delegation_validated",
        "retrieval_eligible",
        "compliance_status",
        "commercial_outcome",
    ):
        assert not hasattr(
            binding,
            attribute,
        )
