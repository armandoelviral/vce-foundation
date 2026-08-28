from dataclasses import FrozenInstanceError

import pytest

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


def create_identity(
    *,
    source_id: str = "POG-2026-DENIM-012",
    source_version: str = "v1.0",
) -> KnowledgeSourceIdentity:
    return KnowledgeSourceIdentity(
        source_id=source_id,
        source_version=source_version,
        source_content_digest=KnowledgeContentDigest(
            algorithm="SHA-256",
            value="0" * 64,
        ),
    )


def create_scope(
    *,
    customer_id: str = "BRAND-CASUAL-X",
) -> KnowledgeSourceScope:
    return KnowledgeSourceScope(
        organization_id="RETAIL-GROUP-GLOBAL",
        customer_id=customer_id,
        jurisdiction="MX",
        commercial_channel_id="PHYSICAL_STORE",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_scope=KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.EXPLICIT,
            ids=(
                "POS-045",
            ),
        ),
        department_scope=KnowledgeScopeSelection(
            mode=KnowledgeScopeMode.EXPLICIT,
            ids=(
                "DPT-DENIM",
            ),
        ),
        campaign_id="CAMP-SPRING-2026",
    )


def create_status(
    **overrides: object,
) -> KnowledgeSourceStatus:
    values = {
        "status_record_id": "KG-STATUS-001",
        "status_version": 1,
        "identity": create_identity(),
        "scope": create_scope(),
        "lifecycle_status": (
            KnowledgeLifecycleStatus.DRAFT
        ),
        "evidence_status": (
            KnowledgeEvidenceStatus.NOT_ASSESSED
        ),
    }
    values.update(overrides)

    return KnowledgeSourceStatus(
        **values,
    )


def test_lifecycle_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeLifecycleStatus) == (
        KnowledgeLifecycleStatus.DRAFT,
        KnowledgeLifecycleStatus.UNDER_REVIEW,
        KnowledgeLifecycleStatus.APPROVED,
        KnowledgeLifecycleStatus.REVOKED,
        KnowledgeLifecycleStatus.ARCHIVED,
    )


def test_evidence_vocabulary_is_exact() -> None:
    assert tuple(KnowledgeEvidenceStatus) == (
        KnowledgeEvidenceStatus.NOT_ASSESSED,
        KnowledgeEvidenceStatus.SUPPORTED,
        KnowledgeEvidenceStatus.DISPUTED,
        KnowledgeEvidenceStatus.INSUFFICIENT_EVIDENCE,
    )


def test_status_preserves_versioned_identity_and_scope() -> None:
    identity = create_identity()
    scope = create_scope()

    status = create_status(
        identity=identity,
        scope=scope,
    )

    assert status.status_record_id == "KG-STATUS-001"
    assert status.status_version == 1
    assert status.identity is identity
    assert status.scope is scope


def test_status_preserves_independent_default_states() -> None:
    status = create_status()

    assert status.lifecycle_status is (
        KnowledgeLifecycleStatus.DRAFT
    )
    assert status.evidence_status is (
        KnowledgeEvidenceStatus.NOT_ASSESSED
    )


def test_approved_lifecycle_can_preserve_disputed_evidence() -> None:
    status = create_status(
        lifecycle_status=(
            KnowledgeLifecycleStatus.APPROVED
        ),
        evidence_status=(
            KnowledgeEvidenceStatus.DISPUTED
        ),
    )

    assert status.lifecycle_status is (
        KnowledgeLifecycleStatus.APPROVED
    )
    assert status.evidence_status is (
        KnowledgeEvidenceStatus.DISPUTED
    )


def test_draft_lifecycle_can_preserve_supported_evidence() -> None:
    status = create_status(
        lifecycle_status=(
            KnowledgeLifecycleStatus.DRAFT
        ),
        evidence_status=(
            KnowledgeEvidenceStatus.SUPPORTED
        ),
    )

    assert status.lifecycle_status is (
        KnowledgeLifecycleStatus.DRAFT
    )
    assert status.evidence_status is (
        KnowledgeEvidenceStatus.SUPPORTED
    )


@pytest.mark.parametrize(
    "invalid_identity",
    (
        "",
        " ",
        None,
        123,
    ),
)
def test_status_rejects_empty_record_identity(
    invalid_identity: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="status_record_id must not be empty",
    ):
        create_status(
            status_record_id=invalid_identity,
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
def test_status_rejects_invalid_version(
    invalid_version: object,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "status_version must be "
            "a positive integer"
        ),
    ):
        create_status(
            status_version=invalid_version,
        )


def test_status_rejects_untyped_source_identity() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "identity must be a "
            "KnowledgeSourceIdentity"
        ),
    ):
        create_status(
            identity="POG-2026-DENIM-012",
        )


def test_status_rejects_untyped_source_scope() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "scope must be a KnowledgeSourceScope"
        ),
    ):
        create_status(
            scope="POS-045",
        )


def test_status_rejects_untyped_lifecycle() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "lifecycle_status must be a "
            "KnowledgeLifecycleStatus"
        ),
    ):
        create_status(
            lifecycle_status="APPROVED",
        )


def test_status_rejects_untyped_evidence_status() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "evidence_status must be a "
            "KnowledgeEvidenceStatus"
        ),
    ):
        create_status(
            evidence_status="SUPPORTED",
        )


def test_status_is_immutable() -> None:
    status = create_status()

    with pytest.raises(FrozenInstanceError):
        status.lifecycle_status = (
            KnowledgeLifecycleStatus.APPROVED
        )


def test_status_versions_can_preserve_same_source_bytes() -> None:
    identity = create_identity()

    draft = create_status(
        status_version=1,
        identity=identity,
        lifecycle_status=(
            KnowledgeLifecycleStatus.DRAFT
        ),
    )
    approved = create_status(
        status_version=2,
        identity=identity,
        lifecycle_status=(
            KnowledgeLifecycleStatus.APPROVED
        ),
    )

    assert draft.identity is approved.identity
    assert (
        draft.identity.source_content_digest
        == approved.identity.source_content_digest
    )
    assert draft != approved


def test_status_does_not_modify_source_identity_or_scope() -> None:
    identity = create_identity()
    scope = create_scope()

    create_status(
        identity=identity,
        scope=scope,
    )

    assert identity.source_id == "POG-2026-DENIM-012"
    assert scope.customer_id == "BRAND-CASUAL-X"


def test_status_does_not_claim_authority_or_applicability() -> None:
    status = create_status(
        lifecycle_status=(
            KnowledgeLifecycleStatus.APPROVED
        ),
    )

    for attribute in (
        "authority_status",
        "authority_source_id",
        "authority_verified",
        "approved_by_actor_id",
        "signature",
        "effective_from",
        "effective_until",
        "temporally_applicable",
        "retrieval_eligible",
        "commercial_outcome",
    ):
        assert not hasattr(
            status,
            attribute,
        )
