from dataclasses import FrozenInstanceError, replace

import pytest

from sp001.contracts.case_read_access import AuthenticatedPrincipal
from sp001.contracts.knowledge_source_scope import (
    KnowledgeDocumentType,
    KnowledgeScopeMode,
    KnowledgeScopeSelection,
    KnowledgeSourceScope,
)
from sp001.contracts.product001_commercial_approval_grant import (
    Product001CommercialApprovalGrant,
    Product001CommercialApprovalOperation,
)


def valid_grant():
    all_scope = KnowledgeScopeSelection(
        mode=KnowledgeScopeMode.ALL,
        ids=(),
    )
    return Product001CommercialApprovalGrant(
        grant_id="grant-001",
        principal=AuthenticatedPrincipal(
            issuer="issuer-001",
            subject="approver-001",
        ),
        operation=(
            Product001CommercialApprovalOperation.APPROVE_PLANOGRAM_VERSION
        ),
        scope=KnowledgeSourceScope(
            organization_id="org-001",
            customer_id="customer-001",
            jurisdiction="MX",
            commercial_channel_id="retail",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=all_scope,
            department_scope=all_scope,
            campaign_id="campaign-001",
        ),
        valid_from=100,
        expires_at=200,
    )


def test_valid_grant_is_immutable():
    grant = valid_grant()
    assert grant.grant_id == "grant-001"
    with pytest.raises(FrozenInstanceError):
        grant.grant_id = "changed"


@pytest.mark.parametrize(
    ("changes", "error"),
    [
        ({"grant_id": ""}, ValueError),
        ({"grant_id": 7}, TypeError),
        ({"principal": "approver"}, TypeError),
        ({"operation": "APPROVE_PLANOGRAM_VERSION"}, TypeError),
        ({"scope": "retail"}, TypeError),
        ({"valid_from": True}, TypeError),
        ({"expires_at": False}, TypeError),
        ({"valid_from": -1}, ValueError),
        ({"expires_at": -1}, ValueError),
        ({"valid_from": 200}, ValueError),
        ({"expires_at": 100}, ValueError),
    ],
)
def test_invalid_grant_is_rejected(changes, error):
    with pytest.raises(error):
        replace(valid_grant(), **changes)


def test_non_planogram_scope_is_rejected():
    grant = valid_grant()
    invalid_scope = replace(
        grant.scope,
        document_type=KnowledgeDocumentType.LOOKBOOK,
    )
    with pytest.raises(ValueError, match="PLANOGRAM"):
        replace(grant, scope=invalid_scope)


def test_grant_does_not_expose_authorization_decision():
    grant = valid_grant()
    assert not hasattr(grant, "is_authorized")
    assert not hasattr(grant, "permits")
