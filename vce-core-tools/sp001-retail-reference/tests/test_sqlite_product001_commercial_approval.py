from dataclasses import replace
import sqlite3

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
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    CommercialApprovalStorageConflict,
    SqliteProduct001CommercialApproval,
)


def grant():
    return Product001CommercialApprovalGrant(
        grant_id="grant-001",
        principal=AuthenticatedPrincipal(
            issuer="issuer", subject="approver"
        ),
        operation=(
            Product001CommercialApprovalOperation
            .APPROVE_PLANOGRAM_VERSION
        ),
        scope=KnowledgeSourceScope(
            organization_id="org",
            customer_id="customer",
            jurisdiction="MX",
            commercial_channel_id="retail",
            document_type=KnowledgeDocumentType.PLANOGRAM,
            point_of_sale_scope=KnowledgeScopeSelection(
                KnowledgeScopeMode.EXPLICIT, ("pos-001",)
            ),
            department_scope=KnowledgeScopeSelection(
                KnowledgeScopeMode.ALL, ()
            ),
            campaign_id="campaign",
        ),
        valid_from=100,
        expires_at=200,
    )


@pytest.fixture
def store(tmp_path):
    return SqliteProduct001CommercialApproval(
        database_path=tmp_path / "commercial.sqlite"
    )


def test_register_and_read(store):
    assert store.register_grant(event_id="e1", grant=grant())
    assert store.read_grant(grant_id="grant-001") == (
        grant(), False
    )


def test_repeated_event_is_idempotent(store):
    assert store.register_grant(event_id="e1", grant=grant())
    assert not store.register_grant(
        event_id="e1", grant=grant()
    )
    assert len(store.read_audit()) == 1


def test_distinct_registration_event_is_audited(store):
    store.register_grant(event_id="e1", grant=grant())
    assert store.register_grant(event_id="e2", grant=grant())
    assert len(store.read_audit()) == 2


def test_event_conflict(store):
    store.register_grant(event_id="e1", grant=grant())
    with pytest.raises(CommercialApprovalStorageConflict):
        store.revoke_grant(event_id="e1", grant=grant())
    assert store.read_grant(grant_id="grant-001")[1] is False


def test_grant_definition_conflict(store):
    store.register_grant(event_id="e1", grant=grant())
    changed = replace(grant(), expires_at=300)
    with pytest.raises(CommercialApprovalStorageConflict):
        store.register_grant(event_id="e2", grant=changed)
    assert len(store.read_audit()) == 1


def test_revoke_and_replay(store):
    store.register_grant(event_id="e1", grant=grant())
    assert store.revoke_grant(event_id="e2", grant=grant())
    assert not store.revoke_grant(
        event_id="e2", grant=grant()
    )
    assert store.read_grant(grant_id="grant-001")[1] is True
    assert len(store.read_audit()) == 2


def test_revocation_is_irreversible(store):
    store.register_grant(event_id="e1", grant=grant())
    store.revoke_grant(event_id="e2", grant=grant())
    with pytest.raises(CommercialApprovalStorageConflict):
        store.register_grant(event_id="e3", grant=grant())
    assert len(store.read_audit()) == 2


def test_missing_grant_cannot_be_revoked(store):
    with pytest.raises(CommercialApprovalStorageConflict):
        store.revoke_grant(event_id="e1", grant=grant())
    assert store.read_audit() == ()


def test_persists_after_reopen(tmp_path):
    path = tmp_path / "commercial.sqlite"
    first = SqliteProduct001CommercialApproval(
        database_path=path
    )
    first.register_grant(event_id="e1", grant=grant())
    second = SqliteProduct001CommercialApproval(
        database_path=path
    )
    assert second.read_grant(grant_id="grant-001") == (
        grant(), False
    )


def test_audit_failure_rolls_back_grant(store):
    with sqlite3.connect(store._path) as connection:
        connection.execute("""
            CREATE TRIGGER reject_commercial_audit
            BEFORE INSERT ON product001_commercial_audit
            BEGIN
                SELECT RAISE(ABORT, 'audit blocked');
            END
        """)
    with pytest.raises(sqlite3.IntegrityError):
        store.register_grant(event_id="e1", grant=grant())
    assert store.read_grant(grant_id="grant-001") is None
    assert store.read_audit() == ()


def test_invalid_event_id(store):
    with pytest.raises(ValueError):
        store.register_grant(event_id="", grant=grant())


def test_invalid_grant(store):
    with pytest.raises(TypeError):
        store.register_grant(event_id="e1", grant=None)
