from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
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
from sp001.contracts.product001_document_version_binding import (
    Product001DocumentVersionBinding,
)
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
    Product001CommercialDecision,
)


def valid_decision():
    return Product001CommercialApprovalDecision(
        decision_id="decision-001",
        document_identity=KnowledgeSourceIdentity(
            source_id="source-001",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value="a" * 64,
            ),
        ),
        document_scope=KnowledgeSourceScope(
            organization_id="org-001",
            customer_id="customer-001",
            jurisdiction="MX",
            commercial_channel_id="retail",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.EXPLICIT,
                ids=("pos-001",),
            ),
            department_scope=KnowledgeScopeSelection(
                mode=KnowledgeScopeMode.ALL,
                ids=(),
            ),
            campaign_id="campaign-001",
        ),
        version_binding=Product001DocumentVersionBinding(
            source_id="source-001",
            commercial_version=1,
            document_version="v1",
            point_of_sale_id="pos-001",
            campaign_id="campaign-001",
        ),
        principal=AuthenticatedPrincipal(
            issuer="issuer-001",
            subject="approver-001",
        ),
        authorization_grant_id="grant-001",
        decision=Product001CommercialDecision.APPROVED,
        decided_at=150,
        evidence_reference="evidence-001",
    )


def test_valid_decision_is_immutable():
    record = valid_decision()
    assert record.decision is Product001CommercialDecision.APPROVED
    with pytest.raises(FrozenInstanceError):
        record.decision_id = "changed"


def test_rejection_is_a_valid_declared_decision():
    record = replace(
        valid_decision(),
        decision=Product001CommercialDecision.REJECTED,
    )
    assert record.decision is Product001CommercialDecision.REJECTED


@pytest.mark.parametrize(
    ("changes", "error"),
    [
        ({"decision_id": ""}, ValueError),
        ({"authorization_grant_id": ""}, ValueError),
        ({"evidence_reference": ""}, ValueError),
        ({"document_identity": "source"}, TypeError),
        ({"document_scope": "scope"}, TypeError),
        ({"version_binding": "binding"}, TypeError),
        ({"principal": "principal"}, TypeError),
        ({"decision": "APPROVED"}, TypeError),
        ({"decided_at": True}, TypeError),
        ({"decided_at": -1}, ValueError),
    ],
)
def test_invalid_decision_is_rejected(changes, error):
    with pytest.raises(error):
        replace(valid_decision(), **changes)


def test_source_mismatch_is_rejected():
    record = valid_decision()
    with pytest.raises(ValueError, match="source identity"):
        replace(
            record,
            version_binding=replace(
                record.version_binding,
                source_id="another-source",
            ),
        )


def test_document_version_mismatch_is_rejected():
    record = valid_decision()
    with pytest.raises(ValueError, match="document version"):
        replace(
            record,
            version_binding=replace(
                record.version_binding,
                document_version="v2",
            ),
        )


def test_campaign_mismatch_is_rejected():
    record = valid_decision()
    with pytest.raises(ValueError, match="campaign"):
        replace(
            record,
            version_binding=replace(
                record.version_binding,
                campaign_id="another-campaign",
            ),
        )


def test_point_of_sale_outside_scope_is_rejected():
    record = valid_decision()
    with pytest.raises(ValueError, match="point of sale"):
        replace(
            record,
            version_binding=replace(
                record.version_binding,
                point_of_sale_id="pos-999",
            ),
        )


def test_non_planogram_document_is_rejected():
    record = valid_decision()
    with pytest.raises(ValueError, match="PLANOGRAM"):
        replace(
            record,
            document_scope=replace(
                record.document_scope,
                document_type=KnowledgeDocumentType.LOOKBOOK,
            ),
        )


def test_decision_does_not_establish_authority():
    record = valid_decision()
    assert not hasattr(record, "is_authorized")
    assert not hasattr(record, "approve")
