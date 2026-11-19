from dataclasses import replace
import sqlite3

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
from sp001.contracts.product001_commercial_approval_grant import (
    Product001CommercialApprovalGrant,
    Product001CommercialApprovalOperation,
)
from sp001.contracts.product001_commercial_approval_decision import (
    Product001CommercialApprovalDecision,
    Product001CommercialDecision,
)
from sp001.infrastructure.sqlite_product001_commercial_approval import (
    SqliteProduct001CommercialApproval,
)
from sp001.infrastructure.sqlite_product001_commercial_decisions import (
    CommercialDecisionDenied,
    CommercialDecisionConflict,
    SqliteProduct001CommercialDecisionWriter,
)


PRINCIPAL = AuthenticatedPrincipal(
    issuer="issuer", subject="approver"
)


def scope():
    return KnowledgeSourceScope(
        organization_id="org",
        customer_id="customer",
        jurisdiction="MX",
        commercial_channel_id="retail",
        document_type=KnowledgeDocumentType.PLANOGRAM,
        point_of_sale_scope=KnowledgeScopeSelection(
            KnowledgeScopeMode.EXPLICIT, ("pos-1",)
        ),
        department_scope=KnowledgeScopeSelection(
            KnowledgeScopeMode.ALL, ()
        ),
        campaign_id="campaign",
    )


def grant():
    return Product001CommercialApprovalGrant(
        grant_id="grant-1",
        principal=PRINCIPAL,
        operation=(
            Product001CommercialApprovalOperation
            .APPROVE_PLANOGRAM_VERSION
        ),
        scope=scope(),
        valid_from=100,
        expires_at=200,
    )


def decision():
    return Product001CommercialApprovalDecision(
        decision_id="decision-1",
        document_identity=KnowledgeSourceIdentity(
            source_id="source-1",
            source_version="v1",
            source_content_digest=KnowledgeContentDigest(
                algorithm="SHA-256",
                value="a" * 64,
            ),
        ),
        document_scope=scope(),
        version_binding=Product001DocumentVersionBinding(
            source_id="source-1",
            commercial_version=1,
            document_version="v1",
            point_of_sale_id="pos-1",
            campaign_id="campaign",
        ),
        principal=PRINCIPAL,
        authorization_grant_id="grant-1",
        decision=Product001CommercialDecision.APPROVED,
        decided_at=150,
        evidence_reference="evidence-1",
    )


@pytest.fixture
def environment(tmp_path):
    path = tmp_path / "commercial.sqlite"
    grants = SqliteProduct001CommercialApproval(
        database_path=path
    )
    now = [150]
    writer = SqliteProduct001CommercialDecisionWriter(
        database_path=path, clock=lambda: now[0]
    )
    return path, grants, writer, now


def save(writer, value=None, principal=PRINCIPAL):
    return writer.save_decision(
        decision=value or decision(),
        authenticated_principal=principal,
    )


def count(path, table):
    with sqlite3.connect(path) as connection:
        return connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]


def test_valid_decision_and_audit(environment):
    path, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    assert save(writer)
    assert count(path, "product001_commercial_decisions") == 1
    assert count(path, "product001_commercial_decision_audit") == 1


def test_identical_replay(environment):
    path, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    assert save(writer)
    assert not save(writer)
    assert count(path, "product001_commercial_decision_audit") == 1


def test_missing_grant_denied(environment):
    path, _, writer, _ = environment
    with pytest.raises(CommercialDecisionDenied):
        save(writer)
    assert count(path, "product001_commercial_decisions") == 0


def test_revoked_grant_denied(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    grants.revoke_grant(event_id="g2", grant=grant())
    with pytest.raises(CommercialDecisionDenied):
        save(writer)


def test_replay_after_revocation_denied(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    save(writer)
    grants.revoke_grant(event_id="g2", grant=grant())
    with pytest.raises(CommercialDecisionDenied):
        save(writer)


@pytest.mark.parametrize("timestamp", [99, 200, 201])
def test_outside_validity_denied(environment, timestamp):
    _, grants, writer, now = environment
    grants.register_grant(event_id="g1", grant=grant())
    now[0] = timestamp
    with pytest.raises(CommercialDecisionDenied):
        save(writer)


def test_wrong_authenticated_principal_denied(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    other = AuthenticatedPrincipal(
        issuer="issuer", subject="other"
    )
    with pytest.raises(CommercialDecisionDenied):
        save(writer, principal=other)


def test_wrong_document_scope_denied(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    altered_scope = replace(scope(), customer_id="other")
    with pytest.raises(CommercialDecisionDenied):
        save(writer, replace(
            decision(), document_scope=altered_scope
        ))


def test_bound_pos_outside_grant_denied(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    broad = replace(
        scope(),
        point_of_sale_scope=KnowledgeScopeSelection(
            KnowledgeScopeMode.ALL, ()
        ),
    )
    altered = replace(
        decision(),
        document_scope=broad,
        version_binding=replace(
            decision().version_binding,
            point_of_sale_id="pos-2",
        ),
    )
    with pytest.raises(CommercialDecisionDenied):
        save(writer, altered)


def test_decision_id_conflict(environment):
    _, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    save(writer)
    with pytest.raises(CommercialDecisionConflict):
        save(writer, replace(
            decision(), evidence_reference="different"
        ))


def test_audit_failure_rolls_back_decision(environment):
    path, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())
    with sqlite3.connect(path) as connection:
        connection.execute("""
            CREATE TRIGGER reject_decision_audit
            BEFORE INSERT ON product001_commercial_decision_audit
            BEGIN
                SELECT RAISE(ABORT, 'audit blocked');
            END
        """)
    with pytest.raises(sqlite3.IntegrityError):
        save(writer)
    assert count(path, "product001_commercial_decisions") == 0
    assert count(path, "product001_commercial_decision_audit") == 0


def test_invalid_clock_denied(environment):
    _, grants, writer, now = environment
    grants.register_grant(event_id="g1", grant=grant())
    now[0] = True
    with pytest.raises(ValueError):
        save(writer)


def test_revocation_committed_before_writer_lock_denies(environment):
    """A queued decision must observe a committed revocation."""
    import threading
    import time

    path, grants, writer, _ = environment
    grants.register_grant(event_id="g1", grant=grant())

    locked = threading.Event()
    release = threading.Event()
    result = []

    def revoke_under_lock():
        connection = sqlite3.connect(
            path, timeout=5.0, isolation_level=None
        )
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "UPDATE product001_commercial_grants "
                "SET revoked=1 WHERE grant_id=?",
                ("grant-1",),
            )
            locked.set()
            if not release.wait(timeout=5):
                raise TimeoutError("test release timeout")
            connection.execute("COMMIT")
        except BaseException:
            if connection.in_transaction:
                connection.execute("ROLLBACK")
            raise
        finally:
            connection.close()

    def attempt_decision():
        try:
            save(writer)
            result.append("accepted")
        except CommercialDecisionDenied:
            result.append("denied")
        except BaseException as exc:
            result.append(type(exc).__name__)

    revoker = threading.Thread(target=revoke_under_lock)
    revoker.start()
    assert locked.wait(timeout=5)

    approver = threading.Thread(target=attempt_decision)
    approver.start()

    try:
        time.sleep(0.05)
    finally:
        release.set()
        revoker.join(timeout=5)
        approver.join(timeout=5)

    assert not revoker.is_alive()
    assert not approver.is_alive()
    assert result == ["denied"]
    assert count(path, "product001_commercial_decisions") == 0
    assert count(path, "product001_commercial_decision_audit") == 0
